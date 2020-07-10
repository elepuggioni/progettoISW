from django import forms
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
            max_length=50,
            min_length=3,
            required=False
        )
        data_scadenza = forms.DateField(
            label="Data scadenza",
            required=False,
            widget=forms.SelectDateWidget(empty_label=('anno', 'mese', 'giorno')),
        )
        story_points = forms.IntegerField(
            label="Story points",
            max_value=20,  # si può togliere, ho dato un valore per ricordarci che esiste la possibilità
            required=False
        )
        colonna = forms.ModelChoiceField(
            queryset=queryset,
            to_field_name='nome'
        )
    return CardForm(*args, **kwargs)