from django import forms
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DatePickerInput
from ScrumBoard.models import *


def add_board(utente_loggato, *args, **kwargs):
    # i superutenti o amministratori sono diretti utilizzatori dell'app?
    # escludo dalla lista anche l'utente che è loggato in questo momento perché è ovvio che ne farà parte
    queryset = User.objects.exclude(is_superuser=True).exclude(id=utente_loggato.id)

    class BoardForm(forms.Form):
        nome = forms.CharField(
            label="Nome board",
            max_length=24,
            min_length=3
        )
        # il proprietario dovrebbe essere colui che crea la board
        """proprietario = forms.ModelChoiceField(
            queryset=queryset,
            to_field_name='username'
        )"""
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


def add_user(utente_loggato, *args, **kwargs):
    queryset = User.objects.exclude(is_superuser=True).exclude(id=utente_loggato.id)

    class UserForm(forms.Form):
        user = forms.ModelMultipleChoiceField(
            queryset=queryset,
            to_field_name='username',
            label='partecipanti'
        )
    return UserForm(*args, **kwargs)

def crea_card_form(board, *args, **kwargs):
    queryset = Colonna.objects.filter(board=board)
    utenti = User.objects.exclude(is_superuser=True)

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
        membri = forms.ModelMultipleChoiceField(
            queryset=utenti,
            to_field_name='username',
            label='membri'
        )
    return CardForm(*args, **kwargs)