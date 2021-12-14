from django.db.models import fields
from django.forms import ModelForm
from django import forms
from django.forms import widgets
from django.forms.widgets import CheckboxInput, TextInput
from .models import brinco, cabecagado, cria, transacao
import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class NumberInput(forms.NumberInput):
    input_type = "number"

class CabecagadoCreateForm(ModelForm):
    class Meta:
        model = cabecagado
        fields = ["n_etiqueta", "brinco","nascimento","sexo"]
        widgets = {
        'n_etiqueta': NumberInput(),
        'nascimento':DateInput()
        }

class CriaCreateForm(ModelForm):
    class Meta:
        model = cria
        fields = ['matriz']

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
            'valor':NumberInput()
        }