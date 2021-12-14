from django.db import models
from django.db.models.base import Model
from django.db.models.fields import AutoField, BooleanField, DateField, FloatField, IntegerField, TextField,CharField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.conf import settings
from colorfield.fields import ColorField
import datetime
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

    def __str__(self):
        return  self.cor_nome

class cabecagado(models.Model):
    id = AutoField(primary_key=True)
    author = ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    n_etiqueta = IntegerField()
    brinco = ForeignKey(brinco,on_delete=models.CASCADE)
    nascimento = DateField()
    MALE = "Macho"
    FEMALE = "Fêmea"

    SEXO_CHOICES = (
        (MALE, "Macho"),
        (FEMALE, "Fêmea"),
    )
    sexo = models.CharField(max_length=5,
                  choices=SEXO_CHOICES,)
    observacoes = TextField(max_length=280,blank=True,null=True)
    esta_vivo = BooleanField(default=True)
    vendido = BooleanField(default=False)
    morte = DateField(null=True,blank=True)
    causa_mortis = CharField(blank=True,max_length=30,null=True)
    BOI = "Boi"
    MATRIZ = "Vaca"
    CRIA = "Bezerro"

    TIPO_CHOICES = (
        (BOI, "Touro"),
        (MATRIZ, "Vaca"),
        (CRIA,"Bezerro")
    )
    tipo = models.CharField(max_length=7,choices=TIPO_CHOICES,)

    def idade(self):
        dias = (datetime.date.today()-self.nascimento).days
        anos = dias//365
        meses = (dias%365)//30
        dias = ((dias%365)%30)
        return f"{f'{anos} anos, ' if anos else ''}{f'{meses} meses e ' if meses else ''}{dias} dias" 
    
    def __str__(self):
        return  str(self.n_etiqueta) + "/" + str(self.brinco)

    

class boi(models.Model):
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)

class matriz(models.Model):
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)

   # def __str__(self):
    #    return  str(self.cabecagado.n_etiqueta) + "/" + str(self.cabecagado.brinco)

class cria(models.Model):
    id = AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)
    matriz = ForeignKey(matriz,on_delete=models.CASCADE)

class ficha_medica(models.Model):
    id=AutoField(primary_key=True)
    cabecagado = OneToOneField(cabecagado,on_delete=models.CASCADE)
    pesos = CharField(max_length=1024,null=True,default="")
    datas = CharField(max_length=1024,null=True,default="")

class vacinas(models.Model):
    id = AutoField(primary_key=True)
    ficha_medica = OneToOneField(ficha_medica,on_delete=models.CASCADE)
    febre_aftosa = BooleanField(default=False)
    brucelose = BooleanField(default=False)
    clostridioses = BooleanField(default=False)
    botulismo = BooleanField(default=False)
    leptospirose = BooleanField(default=False)
    raiva = BooleanField(default=False)
    ibr_bvd = BooleanField(default=False)



class transacao(models.Model):
    VENDA = "Venda"
    COMPRA = "Compra"
    Transacao_choices = (
        (COMPRA,"Compra"),
        (VENDA,"Venda")
    )
    id = AutoField(primary_key=True)
    tipo = CharField(max_length=6,choices=Transacao_choices) #True para Venda, False para compra
    valor = FloatField()
    envolvido = CharField(max_length=32)
    data = DateField()
    tags = CharField(max_length=100)
    observacoes = CharField(max_length=100)

class cabeca_transacionada(models.Model):
    id = AutoField(primary_key=True)
    transacao = ForeignKey(transacao,on_delete=models.CASCADE)
    cabecagado = ForeignKey(cabecagado,on_delete=models.CASCADE)
