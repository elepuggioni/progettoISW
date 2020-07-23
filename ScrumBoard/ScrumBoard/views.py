from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect

from ScrumBoard.forms import *
from ScrumBoard.models import *
from django.contrib.auth.decorators import login_required


def hello(request):
    return HttpResponse("Hello world")


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')


@login_required(login_url='/login')
def dashboard(request):
    return render(request, "dashboard.html", {'board': Board.objects.filter(partecipanti=request.user)})


@login_required(login_url='/login')
def showboard(request, board_id):
    board = Board.objects.get(pk=board_id)
    if request.user not in board.partecipanti.all():
        raise Http404
    else:
        return render(request, "showboard.html", {'board': board, 'board_id': board_id})


@login_required(login_url='/login')
def showcard(request, card_id):
    card = Card.objects.get(id=card_id)
    board = Board.objects.get(pk=card.colonna.board.id)

    if request.user not in board.partecipanti.all():
        raise Http404
    else:
        try:
            card = Card.objects.get(pk=card_id)
        except Card.DoesNotExist:
            card = None
    return render(request, "showcard.html", {'card': card, 'card_id': card_id})


@login_required(login_url='/login')
def crea_board(request):
    if request.method == "POST":
        board_form = BoardForm(request.user, request.POST)
        if board_form.is_valid():
            new_board = Board(
                nome=board_form.cleaned_data['nome'],
                proprietario=request.user
            )
            new_board.save()
            new_board.partecipanti.set(board_form.cleaned_data['membri'])
            new_board.partecipanti.add(request.user)

            redirect_to = Board.objects.get(pk=new_board.pk)
            return redirect(redirect_to)
    else:
        board_form = BoardForm(request.user)
    return render(request, "crea_board.html", {"form": board_form})


@login_required(login_url='/login')
def aggiungi_card(request, board_id):
    board = Board.objects.get(pk=board_id)

    if request.user not in board.partecipanti.all():
        raise Http404

    if request.method == "POST":
        card_form = CardForm(board_id, request.POST)
        if card_form.is_valid():
            new_card = Card(
                nome=card_form.cleaned_data['nome'],
                descrizione=card_form.cleaned_data['descrizione'],
                data_scadenza=card_form.cleaned_data['data_scadenza'],  # la data di inizio dovrebbe essere automatica
                story_points=card_form.cleaned_data['story_points'],
                colonna=card_form.cleaned_data['colonna'],

            )
            new_card.save()
            new_card.membri.set(card_form.cleaned_data['membri'])

            redirect_to = Board.objects.get(pk=board_id)
            return redirect(redirect_to)
    else:
        card_form = CardForm(board=board_id)
    return render(request, "aggiungi_card.html", {"board": board, "form": card_form})


@login_required(login_url='/login')
def aggiungi_colonna(request, board_id):
    board = Board.objects.get(pk=board_id)

    if request.user not in board.partecipanti.all():
        raise Http404

    if request.method == "POST":
        column_form = ColumnForm(request.POST)
        if column_form.is_valid():
            new_column = Colonna(
                nome=column_form.cleaned_data['nome'],
                board=Board.objects.get(pk=board_id)
            )
            new_column.save()

            redirect_to = Board.objects.get(pk=board_id)
            return redirect(redirect_to)
            # render commentato per il momento
            # return render(request, "showboard.html", {'board': Board.objects.get(pk=board_id), 'board_id': board_id})
    else:
        column_form = ColumnForm()
    return render(request, "aggiungi_colonna.html",
                  {"form": column_form, "board": board})  # aggiungi_colonna.html è un placeholder in attesa di quello vero
    # return render(request, "form_tests/aggiungi_colonna_test.html", {'form':column_form, 'board_id':board_id})


@login_required(login_url='/login')
def aggiungi_utente(request, board_id):
    lista_utenti = User.objects.exclude(is_superuser=True).exclude(id=request.user.id)  # non usato

    board = Board.objects.get(pk=board_id)

    if request.user not in board.partecipanti.all():
        raise Http404

    if request.method == "POST":
        user_form = UserForm(board, data=request.POST)
        if user_form.is_valid():
            board.partecipanti.set(user_form.cleaned_data['membri'])
            board.partecipanti.add(request.user)

            redirect_to = Board.objects.get(pk=board_id)
            return redirect(redirect_to)
    else:
        user_form = UserForm(board, data={'membri': board.partecipanti.all()})
    return render(request, "aggiungi_utente.html", {"board": board, "form": user_form})


@login_required(login_url='/login')  # sarà da cancellare
def modifica_board(request, board_id):
    """Modifica il valore del nome della board"""
    board = Board.objects.get(id=board_id)
    if request.method == "POST":
        board_form = BoardForm(request.POST)
        if board_form.is_valid():
            board.nome = board_form.cleaned_data('nome')
            board.proprietario = board_form.cleaned_data['proprietario']
            board.save()
            board.partecipanti.set(board_form.cleaned_data['membri'])
            return HttpResponse("Board modificata")
    else:
        board_form = BoardForm(data={'nome': board.nome})
    """return render(request, "aggiungi_board.html",
                      {"form": board_form})  # aggiungi_board.html è un placeholder in attesa di quello vero"""
    return render(request, "form_tests/modifica_board_test.html", {'form': board_form})


@login_required(login_url='/login')
def modifica_colonna(request, column_id):
    colonna = Colonna.objects.get(id=column_id)
    board = Board.objects.get(pk=colonna.board_id)

    if request.user not in board.partecipanti.all():
        raise Http404

    if request.method == "POST":
        if 'modifica_nome' in request.POST:  # controllo il "name" nel button per capire quale è stato premuto
            column_form = ColumnForm(request.POST)
            if column_form.is_valid():
                colonna.nome = column_form.cleaned_data['nome']
                colonna.save()

                redirect_to = Board.objects.get(pk=colonna.board_id)
                return redirect(redirect_to)
        elif 'cancella_colonna' in request.POST:  # controllo il "name" nel button per capire quale è stato premuto
            return cancella_colonna(request, column_id)
    else:
        column_form = ColumnForm({'nome': colonna.nome})
        # lista_cards = Card.objects.filter(colonna=column_id)

    """return render(request, "form_tests/modifica_colonna.html",
                      {'form': column_form, 'column_id': column_id, 'cards': lista_cards})"""
    return render(request, "modifica_colonna.html",
                  {'form': column_form, 'column': colonna})


@login_required(login_url='/login')
def modifica_card(request, card_id):
    card = Card.objects.get(id=card_id)
    board = Board.objects.get(pk=card.colonna.board.id)

    if request.user not in board.partecipanti.all():
        raise Http404

    if request.method == "POST":
        card_form = CardForm(board=board.id, data=request.POST)

        if card_form.is_valid():
            card.nome = card_form.cleaned_data['nome']
            card.descrizione = card_form.cleaned_data['descrizione']
            card.data_scadenza = card_form.cleaned_data['data_scadenza']
            card.colonna = card_form.cleaned_data['colonna']
            card.story_points = card_form.cleaned_data['story_points']

            card.save()
            card.membri.set(card_form.cleaned_data['membri'])

            redirect_to = Board.objects.get(pk=board.id)
            return redirect(redirect_to)
    else:
        card_form = CardForm(board=board.id, data={'nome': card.nome,
                                                   'descrizione': card.descrizione,
                                                   'data_scadenza': card.data_scadenza,
                                                   'story_points': card.story_points,
                                                   'colonna': card.colonna,
                                                   'membri': card.membri.all()
                                                   })
        # card_form = filtra_colonne(board=board_id,data=card.__dict__)

    return render(request, "modifica_card.html", {"form": card_form, "card": card})


@login_required(login_url='/login')
def burndown(request, board_id):
    board = Board.objects.get(pk=board_id)

    if request.user not in board.partecipanti.all():
        raise Http404

    context = {
        'board': board
    }
    return render(request, "burndown.html", context)


@login_required(login_url='/login')
def cancella_board(request, board_id):
    """Elimina la board indicata"""
    Board.objects.get(id=board_id).delete()
    return HttpResponseRedirect('dashboard/')


@login_required(login_url='/login')
def cancella_colonna(request, column_id):
    """Elimina la colonna indicata"""
    colonna = Colonna.objects.get(id=column_id)
    board = Board.objects.get(pk=colonna.board_id)

    if request.user not in board.partecipanti.all():
        raise Http404
    else:
        colonna.delete()
        return redirect(board)


@login_required(login_url='/login')
def cancella_card(request, card_id):
    """Elimina la card indicata"""
    card = Card.objects.get(id=card_id)
    board = Board.objects.get(pk=card.colonna.board.id)

    if request.user not in board.partecipanti.all():
        raise Http404
    else:
        card.delete()
        column = Colonna.objects.get(id=card.colonna_id)
        return redirect(column)
