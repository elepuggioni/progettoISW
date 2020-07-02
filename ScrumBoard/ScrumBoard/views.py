from django.http import HttpResponse
from django.shortcuts import render
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
