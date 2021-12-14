from django.db.models import fields
from django.forms import ModelForm
from django import forms
from django.forms import widgets
from django.forms.widgets import TextInput
from .models import brinco, cabecagado, cria, vacinas
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class NumberInput(forms.NumberInput):
    input_type = "number"

class CabecagadoCreateForm(ModelForm):
    class Meta:
        model = cabecagado
        fields = ["sexo","n_etiqueta", "brinco","nascimento",]
        widgets = {
        'n_etiqueta': NumberInput(),
        'nascimento':DateInput()
        }

class CriaCreateForm(ModelForm):
    class Meta:
        model = cria
        fields = ['matriz']

class VacinasCreateForm(ModelForm):
    class Meta:
        model = vacinas
        fields = ("febre_aftosa", "brucelose", "clostridioses", "botulismo", "leptospirose", "raiva", "ibr_bvd")

class PesosCreateForm(forms.Form):
    timeseries = forms.TextInput()

class TransacaoCreateForm(ModelForm):
    class Meta:
        model = transacao
        fields = ['valor', 'envolvido', 'data', 'tags', 'observacoes','tipo']
        labels = {'valor':"Valor da transação", 
        'envolvido':"Envolvido", 
        'data':"Data da transição:", 
        'tags':"Identificação da(s) cabeça(s) de gado:",
        'observacoes':"Observações:"
        }
        widgets = {
            'data':DateInput(),
            'valor':NumberInput(),
            'tipo': CheckboxInput()
        }
class TransacaoCreateForm(ModelForm):
    class Meta:
        model = transacao
        fields = ['valor', 'envolvido', 'data', 'tags', 'observacoes','tipo']
        labels = {'valor':"Valor da transação", 
        'envolvido':"Envolvido", 
        'data':"Data da transição:", 
        'tags':"Identificação da(s) cabeça(s) de gado:",
        'observacoes':"Observações:"
        }
        widgets = {
            'data':DateInput(),
            'valor':NumberInput(),
            'tipo': CheckboxInput()
        } 