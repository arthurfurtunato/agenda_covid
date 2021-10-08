from django.db import models
from django.db.models.fields.json import JSONField
from django.contrib.auth.models import User

# Create your models here.

class Cidadao(models.Model):
    nome = models.CharField(max_length=200)
    nascimento = models.DateField()
    cpf = models.CharField(max_length=11)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

class EstabelecimentoSaude(models.Model):
    dados_estabelecimento = JSONField()

class Agendamento(models.Model):
    estabelecimento = models.ForeignKey(EstabelecimentoSaude, on_delete=models.DO_NOTHING)
    cidadao = models.ForeignKey(Cidadao, on_delete=models.DO_NOTHING)
    data_vacinacao = models.DateTimeField()

