from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from ScrumBoard.models import Colonna


class BoardForm(forms.Form):
    nome = forms.CharField(
        label="Nome board",
        max_length=24,
        min_length=3
    )


class ColumnForm(forms.Form):
    nome = forms.CharField(
        label="Nome colonna",
        max_length=16,
        min_length=3
    )


class UserForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=24,
        min_length=3
    )



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