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