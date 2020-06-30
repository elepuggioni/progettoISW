from django.db import models


class Sistema(models.Model):
    pass


class Utente(models.Model):
    nome = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    #lista_board = [] #????

    def login(self):
        pass

    def logout(self):
        pass


class Board(models.Model):
    nome = models.CharField(max_length=32)
    proprietario = models.ForeignKey(Utente, on_delete="CASCADE")
    #lista_utenti = [] #????



class Colonna(models.Model):
    nome = models.CharField(max_length=32)
    board = models.ForeignKey(Board, on_delete="CASCADE")


class Card(models.Model):
    titolo = models.CharField(max_length=32)
    descrizione = models.CharField(max_length=500)
    data_creazione = models.DateField(auto_now_add=True)
    data_scadenza = models.DateField()
    story_points = models.IntegerField()
    colonna = models.ForeignKey(Colonna, on_delete="CASCADE")


