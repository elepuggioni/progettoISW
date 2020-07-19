from django.http import HttpResponse, HttpResponseRedirect
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
    return render(request, "dashboard.html", {'board': Board.objects.filter(proprietario=request.user).union(
        Board.objects.filter(partecipanti=request.user))})


@login_required(login_url='/login')
def card_vuota(request):
    return render(request, "modifica_card.html", {"is_authorized": False})


@login_required(login_url='/login')
def colonna_vuota(request):
    return render(request, "modifica_colonna.html", {'is_authorized': False})


@login_required(login_url='/login')
def board_vuota(request):
    return render(request, "showboard.html", {'is_authorized': False})


@login_required(login_url='/login')
def showboard(request, board_id):
    is_authorized = False

    if not board_id.isdigit():
        return render(request, "showboard.html", {'is_authorized': is_authorized})

    try:
        board = Board.objects.get(pk=board_id)
        auth_users = Board.objects.filter(proprietario=request.user.id).union(
            # utilizzato per raccogliere la lista di utenti
            Board.objects.filter(partecipanti=request.user.id))  # autorizzati ad accedere alla board

        if board in auth_users:
            is_authorized = True

    except Board.DoesNotExist:
        board = None

    return render(request, "showboard.html", {'board': board, 'board_id': board_id, 'is_authorized': is_authorized})


@login_required(login_url='/login')
def showcard(request, card_id):
    try:
        card = Card.objects.get(pk=card_id)
    except Card.DoesNotExist:
        card = None
    return render(request, "showcard.html", {'card': card, 'card_id': card_id})


@login_required(login_url='/login')
def crea_board(request):
    if request.method == "POST":
        board_form = add_board(request.user, request.POST)
        if board_form.is_valid():
            new_board = Board(
                nome=board_form.cleaned_data['nome'],
                proprietario=request.user,
            )
            new_board.save()
            new_board.partecipanti.set(board_form.cleaned_data['membri'])

            redirect_to = Board.objects.get(pk=new_board.pk)
            return redirect(redirect_to)
    else:
        board_form = add_board(request.user)
    return render(request, "crea_board.html", {"form": board_form})


@login_required(login_url='/login')
def aggiungi_card(request, board_id):
    if request.method == "POST":
        card_form = crea_card_form(board_id, request.POST)
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
        card_form = crea_card_form(board=board_id)
    return render(request, "aggiungi_card.html", {"form": card_form})


@login_required(login_url='/login')
def aggiungi_colonna(request, board_id):
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
                  {"form": column_form})  # aggiungi_colonna.html è un placeholder in attesa di quello vero
    # return render(request, "form_tests/aggiungi_colonna_test.html", {'form':column_form, 'board_id':board_id})


@login_required(login_url='/login')
def aggiungi_utente(request, board_id):
    lista_utenti = User.objects.exclude(is_superuser=True).exclude(id=request.user.id)
    board = Board.objects.get(pk=board_id)

    if request.method == "POST":
        user_form = add_user(request.user, data=request.POST)
        if user_form.is_valid():
            board.partecipanti.set(user_form.cleaned_data['membri'])

            redirect_to = Board.objects.get(pk=board_id)
            return redirect(redirect_to)
    else:
        user_form = add_user(request.user, data={'membri': board.partecipanti.all()})
    return render(request, "aggiungi_utente.html", {"form": user_form})


@login_required(login_url='/login')
def modifica_board(request, board_id):
    """Modifica il valore del nome della board"""
    board = Board.objects.get(id=board_id)
    if request.method == "POST":
        board_form = add_board(request.POST)
        if board_form.is_valid():
            board.nome = board_form.cleaned_data('nome')
            board.proprietario = board_form.cleaned_data['proprietario']
            board.save()
            board.partecipanti.set(board_form.cleaned_data['membri'])
            return HttpResponse("Board modificata")
    else:
        board_form = add_board(data={'nome': board.nome})
    """return render(request, "aggiungi_board.html",
                      {"form": board_form})  # aggiungi_board.html è un placeholder in attesa di quello vero"""
    return render(request, "form_tests/modifica_board_test.html", {'form': board_form})


@login_required(login_url='/login')
def modifica_colonna(request, column_id):
    """modifica il nome della colonna"""
    is_authorized = False

    if not column_id.isdigit() or len(column_id) == 0:
        return render(request, "modifica_colonna.html",
                      {'colonna': None, 'is_authorized': is_authorized})

    try:
        colonna = Colonna.objects.get(id=column_id)
        board = Board.objects.get(pk=colonna.board_id)  # ottengo la board a cui appartiene la colonna
        #board_id = card.colonna.board.id

        auth_users = Board.objects.filter(proprietario=request.user.id).union(
            # utilizzato per raccogliere la lista di utenti
            Board.objects.filter(  # autorizzati ad accedere alla board e quindi alla card da modificare
                partecipanti=request.user.id))

        if board in auth_users:
            is_authorized = True

    except Colonna.DoesNotExist:
        colonna = None
        return render(request, "modifica_colonna.html",
                      {'column': colonna, 'is_authorized': is_authorized})

    if request.method == "POST":
        column_form = ColumnForm(request.POST)
        if column_form.is_valid():
            colonna.nome = column_form.cleaned_data['nome'],
            colonna.save()

            redirect_to = Board.objects.get(pk=colonna.board_id)
            return redirect(redirect_to)
    else:
        column_form = ColumnForm({'nome_colonna': colonna.nome})
        lista_cards = Card.objects.filter(colonna=column_id)

    """return render(request, "form_tests/modifica_colonna.html",
                      {'form': column_form, 'column_id': column_id, 'cards': lista_cards})"""
    return render(request, "modifica_colonna.html",
                  {'form': column_form, 'column': colonna, 'cards': lista_cards, 'is_authorized': is_authorized})


@login_required(login_url='/login')
def modifica_card(request, card_id):
    is_authorized = False

    if not card_id.isdigit():
        return render(request, "modifica_card.html",
                      {'card': None, 'is_authorized': is_authorized})

    try:  # try catch per evitare di avere una pagina di errore quando la card non esiste nel db
        card = Card.objects.get(id=card_id)
        board_id = card.colonna.board.id
    except Card.DoesNotExist:
        card = None
        return render(request, "modifica_card.html", {"card": card, "is_authorized": is_authorized})

    board = Board.objects.get(pk=board_id)
    auth_users = Board.objects.filter(proprietario=request.user.id).union(
        # utilizzato per raccogliere la lista di utenti
        Board.objects.filter(  # autorizzati ad accedere alla board e quindi alla card da modificare
            partecipanti=request.user.id))

    if board in auth_users:  # controllo se presente
        is_authorized = True

    if request.method == "POST":
        card_form = crea_card_form(board=board_id, data=request.POST)

        if card_form.is_valid():
            card.nome = card_form.cleaned_data['nome']
            card.descrizione = card_form.cleaned_data['descrizione']
            card.data_scadenza = card_form.cleaned_data['data_scadenza']
            card.colonna = card_form.cleaned_data['colonna']
            card.story_points = card_form.cleaned_data['story_points']

            card.save()
            card.membri.set(card_form.cleaned_data['membri'])

            redirect_to = Board.objects.get(pk=board_id)
            return redirect(redirect_to)
    else:
        card_form = crea_card_form(board=board_id, data={'nome': card.nome,
                                                         'descrizione': card.descrizione,
                                                         'data_scadenza': card.data_scadenza,
                                                         'story_points': card.story_points,
                                                         'colonna': card.colonna,
                                                         'membri': card.membri.all()
                                                         })
        # card_form = filtra_colonne(board=board_id,data=card.__dict__)
    return render(request, "modifica_card.html", {"form": card_form, "card": card, "is_authorized": is_authorized})


@login_required(login_url='/login')
def burndown(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        board = None
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
def cancella_colonna(request, colonna_id):
    """Elimina la colonna indicata"""
    board = Colonna.objects.get(id=colonna_id).board
    Colonna.objects.get(id=colonna_id).delete()
    return HttpResponseRedirect('board/%s/' % str(board.id))


@login_required(login_url='/login')
def cancella_card(request, card_id):
    """Elimina la card indicata"""
    board = Card.objects.get(id=card_id)
    Card.objects.get(id=card_id).delete()
    return HttpResponseRedirect('board/%d/' % board.id)
