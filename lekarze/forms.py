from django import forms
from allauth.account.forms import SignupForm
from django.core.validators import MinValueValidator

from .models import Lekarze


# class LekarzeForm(forms.ModelForm):
#     class Meta:
#         model = Lekarze
#         fields = [
#             'specjalizacja',
#             'numer_gabinetu'
#         ]


# class LekarzeForm2(forms.Form):
#     first_name = forms.CharField(max_length=30, label='Imię')
#     last_name = forms.CharField(max_length=30, label='Nazwisko')
#
#     def signup(self, request, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()


class LekarzeForm(SignupForm):
    specjalizacja = forms.CharField(max_length=25)
    numer_gabinetu = forms.IntegerField(validators=[MinValueValidator(1)])

    def save(self, request):
        user = super(LekarzeForm, self).save(request)

        return user
