from django.db import models


class Board(models.Model):
    """La rappresentazione di una board"""
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Colonna(models.Model):
    """La rappresentazione di una colonna"""
    nome = models.CharField(max_length=50)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
