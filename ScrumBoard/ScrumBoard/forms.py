from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from ScrumBoard.models import *


class BoardForm(forms.Form):
    def __init__(self, utente_loggato, data=None):
        super().__init__(data)
        self.fields['membri'].queryset = User.objects.exclude(id=utente_loggato.id)

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
        queryset=None,
        to_field_name='username',
        label='membri',
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )


class ColumnForm(forms.Form):
    nome = forms.CharField(
        label="Nome colonna",
        max_length=16,
        min_length=3
    )


class UserForm(forms.Form):

    def __init__(self, board, data=None):
        super().__init__(data)
        self.fields['membri'].queryset = User.objects.exclude(id=board.proprietario.id)

    membri = forms.ModelMultipleChoiceField(
        queryset=None,
        to_field_name='username',
        label='membri',
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

class CardForm(forms.Form):
    def __init__(self, board, data=None):
        super().__init__(data)
        self.fields['colonna'].queryset = Colonna.objects.filter(board=board)
        self.fields['membri'].queryset = Board.objects.get(pk=board).partecipanti.all()

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
        queryset=None,
        to_field_name='nome'
    )
    membri = forms.ModelMultipleChoiceField(
        queryset=None,
        to_field_name='username',
        label='membri',
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )