from django.db import models
from django.db.models.fields import AutoField, BooleanField, DateField, FloatField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.conf import settings
# Create your models here.


class UserProfile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name="perfil")
  cargo = models.CharField(max_length=16)

class cabecagado(models.Model):
    id = AutoField(primary_key=True)
    author = ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


class boi(models.Model):
    REQUIRED_FIELDS = ['cabecagado']
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)
    nascimento = DateField(null=True)
    observacoes = TextField(max_length=280,blank=True,null=True)
    esta_vivo = BooleanField(default=True)
    morte = DateField(null=True)
    causa_mortis = TextField(max_length=30,null=True)


class matriz(models.Model):
    REQUIRED_FIELDS = ['cabecagado']
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)
    gestacoes = IntegerField(default=0)
    nascimento = DateField(null=True)
    observacoes = TextField(max_length=280,blank=True,null=True)
    esta_vivo = BooleanField(default=True)
    morte = DateField(null=True)
    causa_mortis = TextField(max_length=30,null=True)

class cria(models.Model):
    REQUIRED_FIELDS = ['cabecagado','nascimento', 'matriz']
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)
    matriz = models.ForeignKey(matriz, on_delete=models.CASCADE)
    nascimento = DateField()
    observacoes = TextField(max_length=280,blank=True,null=True)
    esta_vivo = BooleanField(default=True)
    morte = DateField(null=True)
    causa_mortis = TextField(max_length=30,null=True)

class ficha_medica(models.Model):
    id=AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)
    pesos = TextField(max_length=1024,null=True)
    datas = TextField(max_length=1024,null=True)

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



