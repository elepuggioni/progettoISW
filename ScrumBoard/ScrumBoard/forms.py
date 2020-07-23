from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from ScrumBoard.models import *


def add_board(utente_loggato, *args, **kwargs):
    # i superutenti o amministratori sono diretti utilizzatori dell'app?
    # escludo dalla lista anche l'utente che è loggato in questo momento perché è ovvio che ne farà parte
    queryset = User.objects.exclude(id=utente_loggato.id)

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

        membri = forms.ModelMultipleChoiceField(
            queryset=queryset,
            to_field_name='username',
            label='membri',
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )
    return BoardForm(*args, **kwargs)


class ColumnForm(forms.Form):
    nome = forms.CharField(
        label="Nome colonna",
        max_length=16,
        min_length=3
    )


def add_user(utente_loggato, *args, **kwargs):
    queryset = User.objects.exclude(id=utente_loggato.id)

    class UserForm(forms.Form):
        membri = forms.ModelMultipleChoiceField(
            queryset=queryset,
            to_field_name='username',
            label='membri',
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )
    return UserForm(*args, **kwargs)


def crea_card_form(board, *args, **kwargs):
    queryset = Colonna.objects.filter(board=board)
    utenti = Board.objects.get(pk=board).partecipanti.all()

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
        data_scadenza = forms.DateField(label="Scadenza",
                                        widget=DatePickerInput(format='%d-%m-%Y'),
                                        required=False
                                        )
        story_points = forms.IntegerField(
            label="Story points",
            max_value=20,  # si può togliere, ho dato un valore per ricordarci che esiste la possibilità
            required=False,
            initial=0
        )
        #va messo qualcosa per il quale se non ci sono ancora colonne ti porta a crea colonna
        colonna = forms.ModelChoiceField(
            queryset=queryset,
            to_field_name='nome'
        )
        membri = forms.ModelMultipleChoiceField(
            queryset=utenti,
            to_field_name='username',
            label='membri',
            required=False,
            widget=forms.CheckboxSelectMultiple()
        )
    return CardForm(*args, **kwargs)