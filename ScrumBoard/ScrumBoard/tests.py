import unittest
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
        # inizializzazione delle board
        self.board1 = Board(nome='Board1')
        self.board1.save()
        self.board2 = Board(nome='Board2')
        self.board2.save()
        self.board3 = Board(nome='Board3')
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

    def testFindModels(self):
        # test sulle board
        self.assertEqual(len(Board.objects.all()), 3)

        # test sulle colonne
        self.assertEqual(len(Colonna.objects.all()), 4)
        self.assertIn(self.colonna1, self.board1.colonna_set.all())
        self.assertIn(self.colonna2, self.board1.colonna_set.all())
        self.assertIn(self.colonna3, self.board1.colonna_set.all())
        self.assertIn(self.colonna4, self.board3.colonna_set.all())


if __name__ == '__main__':
    unittest.main()
