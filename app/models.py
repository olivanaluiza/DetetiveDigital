from django.db import models

# 1. Tabela de Usuários
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, verbose_name="Nome")
    email = models.CharField(max_length=100, unique=True, verbose_name="E-mail")
    senha = models.CharField(max_length=255, verbose_name="Senha")
    data_cadastro = models.DateField(auto_now_add=True, verbose_name="Data de Cadastro")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


# 2. Tabela de Quizzes
class Quiz(models.Model):
    id_quiz = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    nivel = models.CharField(max_length=20, verbose_name="Nível")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"


# 3. Tabela de Perguntas
class Pergunta(models.Model):
    id_pergunta = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='id_quiz', verbose_name="Quiz")
    enunciado = models.TextField(verbose_name="Enunciado")
    explicacao = models.TextField(verbose_name="Explicação")

    def __str__(self):
        return f"{self.quiz.titulo} - {self.enunciado[:30]}"

    class Meta:
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"


# 4. Tabela de Alternativas
class Alternativa(models.Model):
    id_alternativa = models.AutoField(primary_key=True)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, db_column='id_pergunta', verbose_name="Pergunta")
    texto = models.CharField(max_length=255, verbose_name="Texto")
    correta = models.BooleanField(default=False, verbose_name="É Correta")

    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"


# 5. Tabela de Tentativas / Ranking 
class TentativaQuiz(models.Model):
    id_tentativa = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', verbose_name="Usuário")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, db_column='id_quiz', verbose_name="Quiz")
    pontuacao = models.IntegerField(verbose_name="Pontuação")
    data_realizacao = models.DateField(auto_now_add=True, verbose_name="Data de Realização")

    def __str__(self):
        return f"{self.usuario.nome} - {self.quiz.titulo} ({self.pontuacao} pts)"

    class Meta:
        verbose_name = "Tentativa do Quiz"
        verbose_name_plural = "Tentativas dos Quizzes"


# 6. Tabela de Denúncias 
class Denuncia(models.Model):
    id_denuncia = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario', verbose_name="Usuário")
    tipo_golpe = models.CharField(max_length=100, verbose_name="Tipo do Golpe")
    descricao = models.TextField(verbose_name="Descrição")
    data_registro = models.DateField(auto_now_add=True, verbose_name="Data do Registro")
    status = models.CharField(max_length=20, default='Pendente', verbose_name="Status") # <-- Campo status incluído!

    def __str__(self):
        return f"{self.tipo_golpe} - {self.usuario.nome}"

    class Meta:
        verbose_name = "Denúncia"
        verbose_name_plural = "Denúncias"