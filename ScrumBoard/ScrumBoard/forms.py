from django import forms


class BoardForm(forms.Form):
    nome_board = forms.CharField(
        label="Nome board",
        max_length=24,
        min_lenght=3
    )

class CardForm(forms.Form):
    nome_card = forms.CharField(
        label="Nome card",
        max_length=24,
        min_lenght=3
    )
    descrizione = forms.CharField(
        label="Descrizione",
        max_length=50,
        min_lenght=3
    )
    data_scadenza = forms.DateField(
        label="Data scadenza"
    )
    story_points = forms.IntegerField(
        label="Story points",
        max_value=20  # si può togliere, ho dato un valore per ricordarci che esiste la possibilità
    )


class ColumnForm(forms.Form):
    nome_colonna = forms.CharField(
        label="Nome colonna",
        max_length=24,
        min_lenght=3
    )


class UserForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=24,
        min_lenght=3
    )