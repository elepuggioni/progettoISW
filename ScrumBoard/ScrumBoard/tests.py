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
        # inizializzazione client
        self.client = Client()

        # inizializzazione degli utenti

        self.utente = User(username="Elena", password="admin")
        self.utente.save()
        """"
        self.utente2 = User(username="Cristina", password="admin")
        self.utente2.save()

        self.utente3 = User(username="Francesco", password="admin")
        self.utente3.save()

        # inizializzazione delle board
        self.boards[0] = Board(nome='boards[0]', proprietario=self.utente)
        self.boards[0].save()

        self.boards[1] = Board(nome='boards[1]', proprietario=self.utente2)
        self.boards[1].save()

        self.boards[2] = Board(nome='boards[2]', proprietario=self.utente3)
        self.boards[2].save()
        """

        # inizializzazione delle boards
        self.boards = []
        self.boards.append(Board(nome='Board1'))
        self.boards.append(Board(nome='Board2'))
        self.boards.append(Board(nome='Board3'))
        for board in self.boards:
            board.save()



        # inizializzazione delle colonne
        self.colonne = []
        self.colonne.append(Colonna(nome='Colonna1', board=self.boards[0]))
        self.colonne.append(Colonna(nome='Colonna2', board=self.boards[0]))
        self.colonne.append(Colonna(nome='Colonna3', board=self.boards[0]))
        self.colonne.append(Colonna(nome='Colonna4', board=self.boards[2]))
        for colonna in self.colonne:
            colonna.save()

        #inizializzazione delle carte
        self.cards = []
        self.cards.append(Card(nome="Prova",
                        descrizione="Carta di prova",
                        story_points="5",
                        data_scadenza=datetime.date.today() - datetime.timedelta(days=3),
                        colonna=self.colonne[0]))
        self.cards.append(Card(nome="Prova2",
                        descrizione="Carta di prova2",
                        story_points="3",
                        data_scadenza=datetime.date.today() + datetime.timedelta(days=3),
                        colonna=self.colonne[1]))
        self.cards.append(Card(nome="Prova3",
                               descrizione="Carta di prova3",
                               story_points="5",
                               data_scadenza=datetime.date.today(),
                               colonna=self.colonne[1]))
        self.cards.append(Card(nome="Completed Card",
                               descrizione="Una carta che ha completato il suo ciclo",
                               story_points=10,
                               data_scadenza=datetime.date.today() + datetime.timedelta(days=5),
                               colonna=self.boards[0].get_ultima_colonna()))
        for card in self.cards:
            card.save()

    def testFindBoards(self):
        # test sulle board
        self.assertEqual(len(Board.objects.all()), len(self.boards))
        for board in self.boards:
            self.assertIn(board, Board.objects.all())
        #self.assertEqual(Board.objects.get(proprietario=self.utente).proprietario, self.utente)

    def testFindColonne(self):
        # test sulle colonne
        self.assertEqual(len(Colonna.objects.all()), len(self.colonne))
        for colonna in self.colonne:
            self.assertIn(colonna, Colonna.objects.all())

    def testFindCards(self):
        # test sulle card
        self.assertEqual(len(Card.objects.all()), len(self.cards))
        for card in self.cards:
            self.assertIn(card, Card.objects.all())

        # si può pensare di usare questo test per eliminare tutti i successivi
        self.assertEqual(self.cards, list(Card.objects.all()))

        self.assertEqual(Card.objects.get(nome='Prova'), self.cards[0])
        self.assertEqual(Card.objects.get(nome='Prova2'), self.cards[1])
        #self.assertEqual(len(Card.objects.all().filter(nome__contains="Prova")), 3)
        #self.assertEqual(len(Card.objects.all().filter(nome__contains="Prova2")), 1)
        #self.assertEqual(len(Card.objects.all().filter(nome__contains="Prova3")), 1)
        #self.assertEqual(len(Card.objects.all().filter(descrizione__contains="Carta di prova")), 3)
        #self.assertEqual(len(Card.objects.all().filter(descrizione__contains="Carta di prova2")), 1)
        #self.assertEqual(len(Card.objects.all().filter(story_points="5")), 2)
        self.assertIn(self.cards[0], self.colonne[0].card_set.all())
        self.assertIn(self.cards[1], self.colonne[1].card_set.all())

    def testNumeroColonne(self):
        self.assertEqual(self.boards[0].num_colonne(), self.contaColonne(self.boards[0]))
        self.assertEqual(self.boards[2].num_colonne(), self.contaColonne(self.boards[2]))

    def contaColonne(self, board):
        count = 0
        for colonna in self.colonne:
            if colonna.board == board:
                count += 1
        return count

    def testNumeroCarteInColonna(self):
        self.assertEqual(self.colonne[0].num_carte(), self.contaCarteColonna(self.colonne[0]))
        self.assertEqual(self.colonne[1].num_carte(), self.contaCarteColonna(self.colonne[1]))

    def contaCarteColonna(self, colonna):
        count = 0
        for card in self.cards:
            if card.colonna == colonna:
                count += 1
        return count

    def testNumeroCarteInBoard(self):
        self.assertEqual(self.boards[0].num_carte(), self.contaCarteBoard(self.boards[0]))

    def contaCarteBoard(self, board):
        count = 0
        for colonna in self.colonne:
            if colonna.board == board:
                count += self.contaCarteColonna(colonna)
        return count

    def testIsScaduta(self):
        self.assertTrue(self.cards[0].is_scaduta())
        self.assertFalse(self.cards[1].is_scaduta())
        self.assertFalse(self.cards[2].is_scaduta())

        # una card nell'ultima colonna non può essere scaduta
        self.assertFalse(self.cards[3].is_scaduta())

    def testContaScadute(self):
        self.assertEqual(self.boards[0].conta_scadute(), self.contaScadute(self.boards[0]))

    def contaScadute(self, board):
        count = 0
        for card in self.cards:
            if (card.colonna.board == board and card.is_scaduta()):
                count += 1
        return count

    def testContaStorypointsUsati(self):
        self.assertEqual(self.boards[0].conta_storypoints_usati(), self.contaStorypointsUsati(self.boards[0]))

    def contaStorypoints(self, colonna):
        totale = 0
        for card in self.cards:
            if (card.colonna == colonna):
                totale += card.story_points
        return totale

    def contaStorypointsUsati(self, board):
        return self.contaStorypoints(board.get_ultima_colonna())


    def testDashboardView(self):
        response = self.client.get('/dashboard/')
        for board in self.boards:
            self.assertContains(response, board.nome)

    def testShowBoard(self):
        response = self.client.get(self.boards[0].get_absolute_url())
        for colonna in Colonna.objects.filter(board=self.boards[0]):
            self.assertContains(response, colonna.nome)
            for card in Card.objects.filter(colonna=colonna):
                self.assertContains(response, card.nome)

if __name__ == '__main__':
    unittest.main()