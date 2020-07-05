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


def crea_board(request):
    if request.method == "POST":
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            new_board = Board(
                nome=board_form.cleaned_data['nome_board']
            )
            new_board.save()
            # da assegnare ad un utente a seconda di come decidiamo di gestire il tutto
            return HttpResponse("Board creata")
    else:
        board_form = BoardForm()
    return render(request, "aggiungi_board.html",
                  {"form": board_form})  # aggiungi_board.html è un placeholder in attesa di quello vero


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


def aggiungi_colonna(request, board_id):
    if request.method == "POST":
        column_form = ColumnForm(request.POST)
        if column_form.is_valid():
            new_column = Colonna(
                nome=column_form.cleaned_data['nome_colonna'],
                board=Board.objects.get(pk=board_id)
            )
            new_column.save()
            return HttpResponse("Colonna aggiunta")
    else:
        column_form = ColumnForm()
    return render(request, "aggiungi_colonna.html",
                  {"form": column_form})  # aggiungi_colonna.html è un placeholder in attesa di quello vero


def aggiungi_utente(request, board_id):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            new_user = User.objects.filter(username=user_form.cleaned_data['username'])
            if not new_user.exists():  # controllo che esista lo username specficato
                return HttpResponse("Username non registrato")
            board = Board.objects.get(pk=board_id)
            # aggiunta utente qui
            # board.partecipanti.append(new_user) o qualcos altro a seconda di come gestiamo questa parte
            return HttpResponse("Utente aggiunto alla board")
    else:
        user_form = UserForm()
    return render(request, "aggiungi_utente.html",
                  {"form": user_form})  # aggiungi_utente è un placeholder in attesa di quello vero
