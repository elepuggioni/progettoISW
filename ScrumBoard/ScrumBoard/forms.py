from django import forms
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput
from ScrumBoard.models import *


def add_board(*args, **kwargs):
    queryset = User.objects.all()

    class BoardForm(forms.Form):
        nome = forms.CharField(
            label="Nome board",
            max_length=24,
            min_length=3
        )
        proprietario = forms.ModelChoiceField(
            queryset=queryset,
            to_field_name='username'
        )
        #lo stile di questo non è finito
        partecipanti = forms.ModelMultipleChoiceField(
            queryset=queryset,
            to_field_name='username',
            label='partecipanti'
            #widget=forms.CheckboxSelectMultiple() #forse
        )
    return BoardForm(*args, **kwargs)


class ColumnForm(forms.Form):
    nome = forms.CharField(
        label="Nome colonna",
        max_length=16,
        min_length=3
    )


def add_user(*args, **kwargs):
    queryset = User.objects.all()

    class UserForm(forms.Form):
        user = forms.ModelMultipleChoiceField(
            queryset=queryset,
            to_field_name='username',
            label='partecipanti'
        )
    return UserForm(*args, **kwargs)

def filtra_colonne(board, *args, **kwargs):
    queryset = Colonna.objects.filter(board=board)

    class CardForm(forms.Form):
        nome = forms.CharField(
            label="Nome card",
            max_length=24,
            min_length=3
        )
        descrizione = forms.CharField(
            label="Descrizione",
            widget=forms.Textarea(attrs={"rows": 5, "cols": 20}),
            max_length=500,
            required=False
        )
        data_scadenza = forms.DateField(label="Scadenza", widget=DatePickerInput(format='%d-%m-%Y'))

        story_points = forms.IntegerField(
            label="Story points",
            max_value=20,  # si può togliere, ho dato un valore per ricordarci che esiste la possibilità
            required=False,
            initial=0
        )
        colonna = forms.ModelChoiceField(
            queryset=queryset,
            to_field_name='nome'
        )
    return CardForm(*args, **kwargs)