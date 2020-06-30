from django.db import models


class Sistema(models.Model):
    pass


class Utente(models.Model):
    nome = models.CharField(max_length=16)
    password = models.CharField(max_length=16)

    # lista_board = [] #????

    @property
    def __str__(self):
        return self.nome

    def login(self):
        pass

    def logout(self):
        pass


class Board(models.Model):
    nome = models.CharField(max_length=32)
    proprietario = models.ForeignKey(Utente, on_delete="CASCADE")

    # lista_utenti = [] #????

    @property
    def __str__(self):
        return '{} ({})'.format(self.nome, self.proprietario)


class Colonna(models.Model):
    nome = models.CharField(max_length=32)
    board = models.ForeignKey(Board, on_delete="CASCADE")

    def __str__(self):
        return '{} - {}'.format(self.nome, self.board)


class Card(models.Model):
    titolo = models.CharField(max_length=32)
    descrizione = models.CharField(max_length=500)
    data_creazione = models.DateField(auto_now_add=True)
    data_scadenza = models.DateField()
    story_points = models.IntegerField()
    colonna = models.ForeignKey(Colonna, on_delete="CASCADE")

    @property
    def __str__(self):
        return 'Titolo: {} \nCreazione: {} \nScadenza: {} \nStory points: {} \nColonna: [{}]'.format(self.titolo,
                                                                                                     self.descrizione,
                                                                                                     self.data_creazione,
                                                                                                     self
                                                                                                     .data_scadenza,
                                                                                                     self.story_points,
                                                                                                     self.colonna)
