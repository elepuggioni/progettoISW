import unittest
import datetime
from django.test import TestCase, Client
from ScrumBoard.models import *


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def testMainPageView(self):
        response = self.client.get("/main/")
        self.assertContains(response, "Prova pagina")


class ModelTest(TestCase):
    def setUp(self):
        persona = Utente(nome="Elena", password="admin")
        persona.save()

        board = Board(nome="Board",
                      proprietario=persona)
        board.save()

        colonna = Colonna(nome="Backlog",
                          board=board)
        colonna.save()

        card = Card(titolo="Prova",
                    descrizione="Carta di prova",
                    story_points="5",
                    data_scadenza=datetime.date(2020, 7, 1),
                    colonna=colonna)
        card.save()
        card2 = Card(titolo="Prova2",
                     descrizione="Carta di prova2",
                     story_points="5",
                     data_scadenza=datetime.date(2020, 7, 2),
                     colonna=colonna)
        card2.save()

    def testFindModels(self):
        self.assertEqual(len(Utente.objects.all()), 1)
        self.assertEqual(len(Utente.objects.all().filter(nome__contains="Elena")), 1)
        self.assertEqual(len(Board.objects.all()), 1)
        self.assertEqual(len(Colonna.objects.all()), 1)
        self.assertEqual(len(Card.objects.all()), 2)
        self.assertEqual(len(Card.objects.all().filter(titolo__contains="Prova")), 2)


if __name__ == "__main__":
    unittest.main()
