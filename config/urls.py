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
    path('quiz/<int:pk>/', QuizDetalheView.as_view(), name='detalhe_quiz'),
]
