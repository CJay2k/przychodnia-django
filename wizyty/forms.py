from django import forms

from .models import Wizyty


class DateInput(forms.DateInput):
    input_type = 'date'


class WizytyForm(forms.ModelForm):
    class Meta:
        model = Wizyty
        fields = [
            'data',
            'godzina',
            'opis'
        ]
        widgets = {
            'data': DateInput(),
        }
