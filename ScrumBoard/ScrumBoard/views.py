from django.http import HttpResponse
from django.shortcuts import render
from django import forms

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
            return render(request, "showboard.html", {'board': new_board, 'board_id': new_board.pk})
    else:
        board_form = BoardForm()
    return render(request, "/dashboard/crea_board.html",
                  {"form": board_form})  # aggiungi_board.html è un placeholder in attesa di quello vero
    #return render(request, "form_tests/creaBoardTest.html", {'form':board_form})


def aggiungi_card(request, board_id):
    board = Board.objects.get(id=board_id)
    if request.method == "POST":
        card_form = filtra_colonne(request.POST, board=board_id)

        if card_form.is_valid():
            new_card = Card(
                nome=card_form.cleaned_data['nome_card'],
                descrizione=card_form.cleaned_data['descrizione'],
                data_scadenza=card_form.cleaned_data['data_scadenza'],  # la data di inizio dovrebbe essere automatica
                story_points=card_form.cleaned_data['story_points'],
                colonna=card_form.cleaned_data['colonna']
            )
            new_card.save()
            return render(request, "showboard.html", {'board': Board.objects.get(pk=board_id), 'board_id': board_id})

    else:
        card_form = filtra_colonne(board=board_id)
    return render(request, "aggiungi_card.html",
                  {"form": card_form})  # aggiungi_card.html è un placeholder in attesa di quello vero
    #return render(request, "form_tests/aggiungi_card_test.html", {'form':card_form})


def aggiungi_colonna(request, board_id):
    if request.method == "POST":
        column_form = ColumnForm(request.POST)
        if column_form.is_valid():
            new_column = Colonna(
                nome=column_form.cleaned_data['nome_colonna'],
                board=Board.objects.get(pk=board_id)
            )
            new_column.save()
            return render(request, "showboard.html", {'board': Board.objects.get(pk=board_id), 'board_id': board_id})
    else:
        column_form = ColumnForm()
    return render(request, "aggiungi_colonna.html",
                  {"form": column_form})  # aggiungi_colonna.html è un placeholder in attesa di quello vero
    #return render(request, "form_tests/aggiungi_colonna_test.html", {'form':column_form, 'board_id':board_id})


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

def modifica_board(request, board_id):
    """Modifica il valore del nome della board"""
    board = Board.objects.get(id=board_id)
    if request.method=="POST":
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            board.nome = board_form.cleaned_data('nome_board')
            board.save()
            return HttpResponse("Board modificata")
    else:
        board_form = BoardForm({'nome_board':board.nome})
    """return render(request, "aggiungi_board.html",
                      {"form": board_form})  # aggiungi_board.html è un placeholder in attesa di quello vero"""
    return render(request, "form_tests/modifica_board_test.html", {'form': board_form})

def modifica_colonna(request, colonna_id):
    """modifica il nome della colonna"""
    colonna = Colonna.objects.get(id=colonna_id)
    if request.method == "POST":
        column_form = ColumnForm(request.POST)
        if column_form.is_valid():
            colonna.nome=column_form.cleaned_data['nome_colonna'],
            colonna.save()
            return HttpResponse("Colonna modificata")
    else:
        column_form = ColumnForm({'nome_colonna':colonna.nome})
    """return render(request, "aggiungi_colonna.html",
                  {"form": column_form})  # aggiungi_colonna.html è un placeholder in attesa di quello vero"""
    return render(request, "form_tests/modifica_colonna_test.html", {'form':column_form, 'board_id':colonna_id})

def modifica_card(request, card_id):

    card = Card.objects.get(id=card_id)
    board_id = card.colonna.board.id
    if request.method == "POST":
        card_form = filtra_colonne(data=request.POST, board=board_id)
        if card_form.is_valid():
            card.nome=card_form.cleaned_data['nome_card'],
            card.descrizione=card_form.cleaned_data['descrizione'],
            card.data_scadenza=card_form.cleaned_data['data_scadenza'],  # la data di inizio dovrebbe essere automatica
            card.story_points=card_form.cleaned_data['story_points'],
            card.colonna=card_form.cleaned_data['colonna']
            card.save()
            return HttpResponse("Card aggiunta")
    else:
        card_form = filtra_colonne(board=board_id,
                                   data={'nome_card':card.nome,
                                         'descrizione':card.descrizione,
                                         'data_scadenza':card.data_scadenza,
                                         'story_points':card.story_points,
                                         'colonna':card.colonna
        })
    """return render(request, "aggiungi_card.html",
                  {"form": card_form})  # aggiungi_card.html è un placeholder in attesa di quello vero"""
    return render(request, "form_tests/modifica_card_test.html", {'form':card_form})


def burndown(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        board = None
    context = {
        'board': board
    }
    return render(request, "burndown.html", context)
