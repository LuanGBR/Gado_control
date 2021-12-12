from django.db import models
from django.db.models.base import Model
from django.db.models.fields import AutoField, BooleanField, DateField, FloatField, IntegerField, TextField,CharField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.conf import settings
from colorfield.fields import ColorField
# Create your models here.


class userprofile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name="perfil")
  cargo = models.CharField(max_length=16)

class brinco(models.Model):
    id = AutoField(primary_key=True)
    cor_nome = CharField(max_length=16,unique=True)
    cor = ColorField()

class cabecagado(models.Model):
    id = AutoField(primary_key=True)
    author = ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    n_etiqueta = IntegerField()
    brinco = ForeignKey(brinco,on_delete=models.CASCADE)
    nascimento = DateField()
    MALE = 1
    FEMALE = 0
    MAR = "MAR"

    SEXO_CHOICES = (
        (MALE, "Macho"),
        (FEMALE, "Fêmea"),
    )
    sexo = models.BooleanField(max_length=1,
                  choices=SEXO_CHOICES,)
    observacoes = TextField(max_length=280,blank=True,null=True)
    esta_vivo = BooleanField(default=True)
    morte = DateField(null=True,blank=True)
    causa_mortis = CharField(blank=True,max_length=30,null=True)

class boi(models.Model):
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)

class matriz(models.Model):
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)

class cria(models.Model):
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)
    matriz = ForeignKey(matriz,on_delete=models.CASCADE)

class ficha_medica(models.Model):
    id=AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)
    pesos = CharField(max_length=1024,null=True)
    datas = CharField(max_length=1024,null=True)

class vacinas(models.Model):
    id = AutoField(primary_key=True)
    OneToOneField(ficha_medica,on_delete=models.CASCADE)
    febre_aftosa = BooleanField(default=False)
    brucelose = BooleanField(default=False)
    clostridioses = BooleanField(default=False)
    botulismo = BooleanField(default=False)
    leptospirose = BooleanField(default=False)
    raiva = BooleanField(default=False)
    ibr_bvd = BooleanField(default=False)



class transacao(models.Model):
    id = AutoField(primary_key=True)
    tipo = BooleanField() #True para Venda, False para compra
    valor = FloatField()
    envolvido = CharField(max_length=32)
    data = DateField()

class cabeca_transacionada(models.Model):
    id = AutoField(primary_key=True)
    transacao = ForeignKey(transacao,on_delete=models.CASCADE)
    cabecagado = ForeignKey(cabecagado,on_delete=models.CASCADE)
    
    






