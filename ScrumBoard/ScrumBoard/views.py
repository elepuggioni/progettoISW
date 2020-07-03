from django.http import HttpResponse
from django.shortcuts import render

from ScrumBoard.forms import *
from ScrumBoard.models import *


def hello(request):
    return HttpResponse("Hello world")


def dashboard(request):
    return render(request, "dashboard.html", {'board': Board.objects.all()})


def showboard(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        board = None
    return render(request, "showboard.html", {'board': board, 'board_id': board_id})


def aggiungi_card(request, column_id):
    if request.method == "POST":
        card_form = CardForm(request.POST)
        if card_form.is_valid():
            new_card = Card(
                nome=card_form.cleaned_data['nome_card'],
                descrizione=card_form.cleaned_data['descrizione'],
                data_scadenza=card_form.cleaned_data['data_scadenza'],  # la data di inizio dovrebbe essere automatica
                story_points=card_form.cleaned_data['story_points'],
                colonna=Colonna.objects.get(pk=column_id)
            )
            new_card.save()
            return HttpResponse("Card aggiunta")
    else:
        card_form = CardForm()
    return render(request, "aggiungi_card.html",
                  {"form": card_form})  # aggiungi_card.html è un placeholder in attesa di quello vero
