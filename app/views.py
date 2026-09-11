from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')
    def post(self, request):
        pass

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        usuario_input = request.POST.get('username')
        senha_input = request.POST.get('password')

      # Autentica o usuário com o banco do Django  
        user = authenticate(request, username=usuario_input, password=senha_input)

        if user is not None:
            login(request, user)  # Cria a sessão
            return redirect('index') # Altere para 'perfil' quando a página existir
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return render(request, 'login.html')

class CadastroView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cadastro.html')

    def post(self, request, *args, **kwargs):
        usuario_input = request.POST.get('username')
        email_input = request.POST.get('email')
        senha_input = request.POST.get('password')
        confirma_senha = request.POST.get('confirm_password')

        # Validações básicas
        if senha_input != confirma_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'cadastro.html')

        if User.objects.filter(username=usuario_input).exists():
            messages.error(request, 'Este nome de usuário já está em uso.')
            return render(request, 'cadastro.html')

        # Salva o usuário com senha criptografada no banco
        novo_usuario = User.objects.create_user(
            username=usuario_input,
            email=email_input,
            password=senha_input
        )
        novo_usuario.save()

        # Loga automaticamente após cadastrar
        login(request, novo_usuario)
        return redirect('index')

class PerfilView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'perfil.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

class QuizzesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        quizzes = Quiz.objects.all()
        # Chama a Tela 3 (Lista)
        return render(request, 'quizzes.html', {'quizzes': quizzes})


class QuizDetalheView(View):
    def get(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        perguntas_list = quiz.pergunta_set.all()
        
        pagina_atual = int(request.GET.get('pagina', 1))
        
        # Se estiver recomeçando o quiz (página 1), limpa as respostas salvas na sessão
        if pagina_atual == 1:
            request.session[f'respostas_quiz_{pk}'] = {}

        total_perguntas = perguntas_list.count()
        pergunta = perguntas_list[pagina_atual - 1] if 1 <= pagina_atual <= total_perguntas else None

        # Pontuação acumulada do histórico do usuário
        pontos_acumulados = 0
        if request.user.is_authenticated:
            usuario_custom = Usuario.objects.filter(email=request.user.email).first()
            if usuario_custom:
                tentativas = TentativaQuiz.objects.filter(usuario=usuario_custom)
                pontos_acumulados = sum(t.pontuacao for t in tentativas if t.pontuacao)

        context = {
            'quiz': quiz,
            'pergunta': pergunta,
            'pagina_atual': pagina_atual,
            'total_perguntas': total_perguntas,
            'tem_proxima': pagina_atual < total_perguntas,
            'tem_anterior': pagina_atual > 1,
            'pagina_anterior': pagina_atual - 1,
            'proxima_pagina': pagina_atual + 1,
            'pontos_acumulados': pontos_acumulados,
        }
        return render(request, 'quizzes.html', context)

    def post(self, request, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        perguntas = quiz.pergunta_set.all()
        
        # Recupera as respostas guardadas das páginas anteriores
        chave_sessao = f'respostas_quiz_{pk}'
        respostas_salvas = request.session.get(chave_sessao, {})

        # Grava a resposta da página atual enviada no form
        for key, value in request.POST.items():
            if key.startswith('pergunta_'):
                respostas_salvas[key] = value
        
        request.session[chave_sessao] = respostas_salvas

        pagina_atual = int(request.POST.get('pagina_atual', 1))
        acao = request.POST.get('acao')

        # Se o usuário clicou em "Próxima" ou "Voltar", salva na sessão e redireciona a página
        if acao == 'proxima':
            return redirect(f'/quiz/{pk}/?pagina={pagina_atual + 1}')
        elif acao == 'voltar':
            return redirect(f'/quiz/{pk}/?pagina={pagina_atual - 1}')

        # Se clicou em "Finalizar" (acao == 'finalizar')
        pontuacao_obtida = 0
        for pergunta in perguntas:
            resposta_id = respostas_salvas.get(f'pergunta_{pergunta.id_pergunta}')
            if resposta_id:
                alternativa = Alternativa.objects.filter(id_alternativa=resposta_id, correta=True).first()
                if alternativa:
                    pontuacao_obtida += 100

        # Limpa as respostas da sessão após concluir
        if chave_sessao in request.session:
            del request.session[chave_sessao]

        # Salva a tentativa no banco
        if request.user.is_authenticated:
            usuario_custom = Usuario.objects.filter(email=request.user.email).first()
            if usuario_custom:
                TentativaQuiz.objects.create(
                    usuario=usuario_custom,
                    quiz=quiz,
                    pontuacao=pontuacao_obtida
                )

        context = {
            'quiz': quiz,
            'perguntas': perguntas,
            'pontuacao': pontuacao_obtida,
            'total': perguntas.count() * 100,
            'finalizado': True,
        }
        return render(request, 'quizzes.html', context)
    
class RankingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):

        usuarios = Usuario.objects.all()

        ranking = []

        for usuario in usuarios:

            # Pega todos os quizzes que esse usuário já tentou
            tentativas = TentativaQuiz.objects.filter(
                usuario=usuario
            )

            # Guarda somente a maior pontuação de cada quiz
            maiores_pontuacoes = []

            quizzes_feitos = tentativas.values('quiz').distinct()

            for quiz in quizzes_feitos:

                maior_pontuacao = tentativas.filter(
                    quiz=quiz['quiz']
                ).order_by('-pontuacao').first()

                if maior_pontuacao:
                    maiores_pontuacoes.append(
                        maior_pontuacao.pontuacao
                    )

            # Soma apenas as maiores pontuações
            pontos = sum(maiores_pontuacoes)

            ranking.append({
                'usuario': usuario,
                'pontos': pontos
            })

        # Maior pontuação primeiro
        ranking.sort(
            key=lambda x: x['pontos'],
            reverse=True
        )

        return render(
            request,
            'ranking.html',
            {
                'ranking': ranking
            }
        )