from django.contrib import admin
from django.urls import include, path
from app.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('quizzes/', QuizzesView.as_view(), name='quizzes'),
    path('quiz/<int:pk>/', QuizDetalheView.as_view(), name='quiz_detalhe'),
    path('ranking/', RankingView.as_view(), name='ranking'),
    path('denuncias/', DenunciasView.as_view(), name='denuncias'),
    path('alertas/', AlertasView.as_view(), name='alertas'),
    path('denuncias/<int:id_denuncia>/aprovar/',aprovar_denuncia,name='aprovar_denuncia'),
    path('denuncias/<int:id_denuncia>/rejeitar/',rejeitar_denuncia,name='rejeitar_denuncia'),
    path('contato/', ContatoView.as_view(), name='contato'),
]
