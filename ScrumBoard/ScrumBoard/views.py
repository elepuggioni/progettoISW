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
    return render(request, "dashboard.html", {'board': Board.objects.filter(proprietario=request.user.id).union(
            Board.objects.filter(partecipanti=request.user.id))})


@login_required(login_url='/login')
def card_vuota(request):
    return render(request, "modifica_card.html", {"is_authorized": False})


@login_required(login_url='/login')
def colonna_vuota(request):
    return render(request, "modifica_colonna.html", {'is_authorized': False})


@login_required(login_url='/login')
def cancella_card_vuota(request):
    return render(request, "cancella_card.html", {'is_authorized': False})


@login_required(login_url='/login')
def modifica_card_vuota(request):
    return render(request, "modifica_card.html", {'is_authorized': False})


@login_required(login_url='/login')
def cancella_colonna_vuota(request):
    return render(request, "cancella_colonna.html", {'is_authorized': False})


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
        # utilizzato per trovare la lista di boards associate all'utente
        user_boards = Board.objects.filter(proprietario=request.user.id).union(
            Board.objects.filter(partecipanti=request.user.id))

        if board in user_boards:
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
        board_form = BoardForm(request.user, request.POST)
        if board_form.is_valid():
            new_board = Board(
                nome=board_form.cleaned_data['nome'],
                proprietario=request.user
            )
            new_board.save()
            new_board.partecipanti.set(board_form.cleaned_data['membri'])

            redirect_to = Board.objects.get(pk=new_board.pk)
            return redirect(redirect_to)
    else:
        board_form = BoardForm(request.user)
    return render(request, "crea_board.html", {"form": board_form})


@login_required(login_url='/login')
def aggiungi_card(request, board_id):
    is_authorized = False

    try:
        board = Board.objects.get(pk=board_id)
        # utilizzato per trovare la lista di boards associate all'utente
        user_boards = Board.objects.filter(proprietario=request.user.id).union(
            Board.objects.filter(partecipanti=request.user.id))

        if board in user_boards:
            is_authorized = True

    except Board.DoesNotExist:
        board = None
        is_authorized = False
        return render(request, "aggiungi_card.html",
                      {"board": board, "is_authorized": is_authorized})

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
    return render(request, "aggiungi_card.html", {"board": board, "form": card_form, "is_authorized": is_authorized})


@login_required(login_url='/login')
def aggiungi_colonna(request, board_id):
    is_authorized = False

    try:
        board = Board.objects.get(pk=board_id)
        # utilizzato per trovare la lista di boards associate all'utente
        user_boards = Board.objects.filter(proprietario=request.user.id).union(
            Board.objects.filter(partecipanti=request.user.id))

        if board in user_boards:
            is_authorized = True
    except Board.DoesNotExist:
        board = None
        is_authorized = False
        return render(request, "aggiungi_colonna.html",
                      {"board": board, "is_authorized": is_authorized})

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
                  {"form": column_form, "board": board, "is_authorized": is_authorized})  # aggiungi_colonna.html è un placeholder in attesa di quello vero
    # return render(request, "form_tests/aggiungi_colonna_test.html", {'form':column_form, 'board_id':board_id})


@login_required(login_url='/login')
def aggiungi_utente(request, board_id):
    is_authorized = False

    lista_utenti = User.objects.exclude(is_superuser=True).exclude(id=request.user.id)

    try:
        board = Board.objects.get(pk=board_id)
        # utilizzato per trovare la lista di boards associate all'utente
        user_boards = Board.objects.filter(proprietario=request.user.id).union(
            Board.objects.filter(partecipanti=request.user.id))

        if board in user_boards:
            is_authorized = True

    except Board.DoesNotExist:
        board = None
        return render(request, "aggiungi_utente.html", {"board": board, "is_authorized": is_authorized})

    if request.method == "POST":
        user_form = UserForm(board, data=request.POST)
        if user_form.is_valid():
            board.partecipanti.set(user_form.cleaned_data['membri'])

            redirect_to = Board.objects.get(pk=board_id)
            return redirect(redirect_to)
    else:
        user_form = UserForm(board, data={'membri': board.partecipanti.all()})
    return render(request, "aggiungi_utente.html", {"board": board, "form": user_form, "is_authorized": is_authorized})


@login_required(login_url='/login')
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
    """modifica il nome della colonna"""
    is_authorized = False

    if not column_id.isdigit():
        return render(request, "modifica_colonna.html",
                      {'colonna': None, 'is_authorized': is_authorized})

    try:
        colonna = Colonna.objects.get(id=column_id)
        board = Board.objects.get(pk=colonna.board_id)  # ottengo la board a cui appartiene la colonna
        # board_id = colonna.board_id

        # utilizzato per trovare la lista di boards associate all'utente
        user_boards = Board.objects.filter(proprietario=request.user.id).union(
            Board.objects.filter(partecipanti=request.user.id))

        if board in user_boards:
            is_authorized = True

    except Colonna.DoesNotExist:
        colonna = None
        return render(request, "modifica_colonna.html",
                      {'column': colonna, 'is_authorized': is_authorized})

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
                  {'form': column_form, 'column': colonna, 'is_authorized': is_authorized})


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

    # utilizzato per trovare la lista di boards associate all'utente
    user_boards = Board.objects.filter(proprietario=request.user.id).union(
        Board.objects.filter(partecipanti=request.user.id))

    if board in user_boards:  # controllo se presente
        is_authorized = True

    if request.method == "POST":
        card_form = CardForm(board=board_id, data=request.POST)

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
        card_form = CardForm(board=board_id, data={'nome': card.nome,
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
    is_authorized = False
    try:
        board = Board.objects.get(pk=board_id)
        # utilizzato per trovare la lista di boards associate all'utente
        user_boards = Board.objects.filter(proprietario=request.user.id).union(
            Board.objects.filter(partecipanti=request.user.id))

        if board in user_boards:
            is_authorized = True
    except Board.DoesNotExist:
        board = None
    context = {
        'is_authorized': is_authorized,
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
    column = Colonna.objects.get(id=column_id)
    board = Board.objects.get(pk=column.board_id)

    # utilizzato per trovare la lista di boards associate all'utente questo si può cambiare a solo il proprietario se
    # dovessimo decidere che solo il proprietario può eliminare le colonne
    user_boards = Board.objects.filter(proprietario=request.user.id).union(
        Board.objects.filter(partecipanti=request.user.id))

    if board in user_boards:
        column.delete()
        return redirect(board)

    else:  # nel caso in cui l'utente non faccia parte della stessa board in cui si trova la card
        return render(request, "cancella_colonna.html", {'is_authorized': False})


@login_required(login_url='/login')
def cancella_card(request, card_id):
    """Elimina la card indicata"""

    try:
        card = Card.objects.get(id=card_id)
    except Card.DoesNotExist:
        return render(request, "cancella_card.html", {'is_authorized': False})

    column = Colonna.objects.get(id=card.colonna_id)
    board = Board.objects.get(pk=column.board_id)

    # utilizzato per trovare la lista di boards associate all'utente questo si può cambiare a solo il proprietario se
    # dovessimo decidere che solo il proprietario può eliminare le cards
    user_boards = Board.objects.filter(proprietario=request.user.id).union(
        Board.objects.filter(partecipanti=request.user.id))

    if board in user_boards:
        Card.objects.get(id=card_id).delete()
        return redirect(column)

    else:  # nel caso in cui l'utente non faccia parte della stessa board in cui si trova la card
        return render(request, "cancella_card.html", {'is_authorized': False})
