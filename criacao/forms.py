from django.forms import ModelForm
from django import forms
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