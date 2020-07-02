import unittest
import datetime
from django.test import TestCase, Client
from ScrumBoard.models import *


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def testHelloWorldView(self):
        response = self.client.get('/hello/')
        self.assertContains(response, "Hello world")


class ModelTest(TestCase):

    def setUp(self):

        # inizializzazione degli utenti
        self.utente = User(username="Elena", password="admin")
        self.utente.save()

        self.utente2 = User(username="Cristina", password="admin")
        self.utente2.save()

        self.utente3 = User(username="Francesco", password="admin")
        self.utente3.save()

        # inizializzazione delle board
        self.board1 = Board(nome='Board1', proprietario=self.utente)
        self.board1.save()

        self.board2 = Board(nome='Board2', proprietario=self.utente2)
        self.board2.save()

        self.board3 = Board(nome='Board3', proprietario=self.utente3)
        self.board3.save()

        # inizializzazione delle colonne
        self.colonna1 = Colonna(nome='Colonna1', board=self.board1)
        self.colonna1.save()
        self.colonna2 = Colonna(nome='Colonna2', board=self.board1)
        self.colonna2.save()
        self.colonna3 = Colonna(nome='Colonna3', board=self.board1)
        self.colonna3.save()
        self.colonna4 = Colonna(nome='Colonna4', board=self.board3)
        self.colonna4.save()

        self.card = Card(nome="Prova",
                    descrizione="Carta di prova",
                    story_points="5",
                    data_scadenza=datetime.date(2020, 7, 1),
                    colonna=self.colonna1)
        self.card.save()

        self.card2 = Card(nome="Prova2",
                     descrizione="Carta di prova2",
                     story_points="3",
                     data_scadenza=datetime.date(2020, 7, 2),
                     colonna=self.colonna2)
        self.card2.save()

    def testFindModels(self):
        # test sulle board
        #numero boards
        self.assertEqual(len(Board.objects.all()), 3)
        #test sui campi
        self.assertEqual(Board.objects.get(proprietario=self.utente).proprietario, self.utente)

        # test sulle colonne
        self.assertEqual(len(Colonna.objects.all()), 4)
        self.assertIn(self.colonna1, self.board1.colonna_set.all())
        self.assertIn(self.colonna2, self.board1.colonna_set.all())
        self.assertIn(self.colonna3, self.board1.colonna_set.all())
        self.assertIn(self.colonna4, self.board3.colonna_set.all())

        # test sulle card
        self.assertEqual(len(Card.objects.all()), 2)
        self.assertEqual(len(Card.objects.all().filter(nome__contains="Prova")), 2)
        self.assertEqual(len(Card.objects.all().filter(nome__contains="Prova2")), 1)
        self.assertEqual(len(Card.objects.all().filter(descrizione__contains="Carta di prova")), 2)
        self.assertEqual(len(Card.objects.all().filter(descrizione__contains="Carta di prova2")), 1)
        self.assertEqual(Card.objects.get(story_points="5").story_points, 5)
        self.assertEqual(Card.objects.get(story_points="3").story_points, 3)
        self.assertEqual(Card.objects.get(story_points="5"), self.card)
        self.assertEqual(Card.objects.get(story_points="3"), self.card2)
        self.assertIn(self.card, self.colonna1.card_set.all())
        self.assertIn(self.card2, self.colonna2.card_set.all())
        self.assertEqual(Card.objects.get(data_scadenza=datetime.date(2020, 7, 1)).data_scadenza,
                         datetime.date(2020, 7, 1))
        self.assertEqual(Card.objects.get(data_scadenza=datetime.date(2020, 7, 2)).data_scadenza,
                         datetime.date(2020, 7, 2))
        self.assertEqual(Card.objects.get(data_scadenza=datetime.date(2020, 7, 1)), self.card)
        self.assertEqual(Card.objects.get(data_scadenza=datetime.date(2020, 7, 2)), self.card2)


if __name__ == '__main__':
    unittest.main()