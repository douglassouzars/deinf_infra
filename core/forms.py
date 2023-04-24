from django import forms

class ContatoForm(forms.Form):
    Nome = forms.CharField(label="Nome")