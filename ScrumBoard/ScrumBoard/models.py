from django.db import models
from django.contrib.auth.models import User

# :)))))))))))))
class Utente():
    def show_boards(self):
        #per ogni board presa dal db
        #board.__str__()
        pass


class Board(models.Model):
    """La rappresentazione di una board"""
    nome = models.CharField(max_length=50)
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE)

    #utenti_partecipanti = models.ManyToManyField(User)

    def aggiungi_utente(self, utente):
        pass

    def elimina_utente(self, utente):
        pass

    def cambia_nome(self, nome):
        pass

    def num_colonne(self):
        pass

    def aggiungi_colonna(self, colonna):
        pass

    def elimina_colonna(self, colonna):
        pass

    def conta_storypoints(self):
        #per ogni colonna
        #chiama colonna.conta_storypoints()
        pass

    def aggiungi_card(self):
        #chiama colonna.crea_card()
        pass

    def __str__(self):
        return self.nome


class Colonna(models.Model):
    """La rappresentazione di una colonna"""
    nome = models.CharField(max_length=50)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    is_last = models.BooleanField(default=True)

    def cambia_nome(self, nome):
        self.nome = nome

    def crea_card(self, card):
        pass

    def rimuovi_card(self, card):
        pass

    """ da implementare forse
    def print_lista_card(self): 
        pass
    """
    def aggiorna_ultima_colonna(self):
        pass
        #cerca la colonna is_last = true
        #cambia a false

    def num_carte(self):
        #query al db
        pass

    def conta_storypoints(self):
        pass

    def __str__(self):
        return self.nome


class Card(models.Model):
    nome = models.CharField(max_length=50)
    descrizione = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)
    data_scadenza = models.DateField()
    story_points = models.IntegerField()
    colonna = models.ForeignKey(Colonna, on_delete="CASCADE")

    def aggiungi_utente(self, utente): #utente tipo User
        pass

    def rimuovi_utente(self, utente):
        pass

    def cambia_colonna(self, colonna):
        self.colonna = colonna

    def cambia_nome(self, nome):
        self.nome = nome

    def cambia_descrizione(self, descrizione):
        self.descrizione = descrizione

    def cambia_scadenza(self, scadenza):
        self.data_scadenza = scadenza

    def cambia_storypoints(self, sp):
        self.story_points = sp
