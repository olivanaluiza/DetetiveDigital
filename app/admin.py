from django.contrib import admin
from .models import Usuario, Quiz, Pergunta, Alternativa, TentativaQuiz, Denuncia

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nome', 'email', 'data_cadastro')
    search_fields = ('nome', 'email')
    list_filter = ('data_cadastro',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id_quiz', 'titulo', 'nivel')
    search_fields = ('titulo',)
    list_filter = ('nivel',)

@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('id_pergunta', 'quiz', 'enunciado')
    search_fields = ('enunciado',)
    list_filter = ('quiz',)

@admin.register(Alternativa)
class AlternativaAdmin(admin.ModelAdmin):
    list_display = ('id_alternativa', 'pergunta', 'texto', 'correta')
    list_filter = ('correta', 'pergunta')

@admin.register(TentativaQuiz)
class TentativaQuizAdmin(admin.ModelAdmin):
    list_display = ('id_tentativa', 'usuario', 'quiz', 'pontuacao', 'data_realizacao')
    list_filter = ('quiz', 'data_realizacao')
    search_fields = ('usuario__nome',)

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('id_denuncia', 'usuario', 'tipo_golpe', 'status', 'data_registro')
    search_fields = ('tipo_golpe', 'descricao', 'usuario__nome')
    list_filter = ('status', 'data_registro', 'tipo_golpe')