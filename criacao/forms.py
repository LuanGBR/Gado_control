from django.forms import ModelForm
from django import forms
from django.forms.widgets import TextInput
from .models import brinco, cabecagado
import datetime
class DateInput(forms.DateInput):
    input_type = 'date'

class NumberInput(forms.NumberInput):
    input_type="number"

class CabecagadoCreateForm(ModelForm):
    class Meta:
        model = cabecagado
        fields = ["tipo","n_etiqueta", "brinco","nascimento","sexo"]
        widgets = {
        'n_etiqueta': NumberInput(),
        'nascimento':DateInput()
        }