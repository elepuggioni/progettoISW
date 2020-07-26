import datetime
import time
import unittest

from django.contrib.auth.models import User
from django.test import TestCase, Client, LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ScrumBoard.models import *
from utils import get_chromedriver_path


class ModelTest(TestCase):
    def setUp(self):
        # inizializzazione client
        self.client = Client()

        # inizializzazione degli utenti
        self.utenti = []
        self.utenti.append(User(username="Utente1", password="admin"))
        self.utenti.append(User(username="Utente2", password="admin"))
        self.utenti.append(User(username="Utente3", password="admin"))
        for utente in self.utenti:
            utente.save()

        # inizializzazione delle boards
        self.boards = []
        self.boards.append(Board(nome='Board1', proprietario=self.utenti[0]))
        self.boards.append(Board(nome='Board2', proprietario=self.utenti[1]))
        self.boards.append(Board(nome='Board3', proprietario=self.utenti[2]))
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

        # inizializzazione delle carte
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

        # aggiunta dei partecipanti
        self.boards[0].partecipanti.add(self.utenti[1], self.utenti[2])

    def testFindUtenti(self):
        # test sugli utenti
        self.assertEqual(User.objects.all().count(), len(self.utenti))
        for utente in self.utenti:
            self.assertIn(utente, User.objects.all())

    def testFindBoards(self):
        # test sulle board
        self.assertEqual(len(Board.objects.all()), len(self.boards))
        for board in self.boards:
            self.assertIn(board, Board.objects.all())
        # self.assertEqual(Board.objects.get(proprietario=self.utente).proprietario, self.utente)

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
        # self.assertEqual(len(Card.objects.all().filter(nome__contains="Prova")), 3)
        # self.assertEqual(len(Card.objects.all().filter(nome__contains="Prova2")), 1)
        # self.assertEqual(len(Card.objects.all().filter(nome__contains="Prova3")), 1)
        # self.assertEqual(len(Card.objects.all().filter(descrizione__contains="Carta di prova")), 3)
        # self.assertEqual(len(Card.objects.all().filter(descrizione__contains="Carta di prova2")), 1)
        # self.assertEqual(len(Card.objects.all().filter(story_points="5")), 2)
        self.assertIn(self.cards[0], self.colonne[0].card_set.all())
        self.assertIn(self.cards[1], self.colonne[1].card_set.all())

    def testPartecipanti(self):
        self.assertIn(self.utenti[1], User.objects.filter(partecipanti=self.boards[0]))
        self.assertIn(self.utenti[2], User.objects.filter(partecipanti=self.boards[0]))

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
        return count;

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
        # self.assertTrue(self.client.login(username=self.utenti[0].username, password='admin'))
        self.client.force_login(self.utenti[0])
        response = self.client.get('/dashboard/')
        for board in self.boards:
            if (board.partecipanti == self.utenti[0]):
                self.assertContains(response, board.nome)


"""
    def testShowBoard(self):
        # self.assertTrue(self.client.login(username='Utente1', password='admin'))

        response = self.client.get(self.boards[0].get_absolute_url())
        for colonna in Colonna.objects.filter(board=self.boards[0]):
            self.assertContains(response, colonna.nome)
            for card in Card.objects.filter(colonna=colonna):
                self.assertContains(response, card.nome)

    def testCreaBoardViewGet(self):
        response = self.client.get('/dashboard/crea_board')
        self.assertIsInstance(response.context['fo  rm'], BoardForm)

    def testCreaBoardPost(self):
        response = self.client.post('/dashboard/crea_board', {'nome':'testpipo'})
        print(response.context['nome'])"""

# timeout per i tentativi
timeout = 5


class ViewsTest(LiveServerTestCase):
    def setUp(self):
        # dovete scaricare il driver del browser corrispondente (chrome in questo caso)
        # da https://sites.google.com/a/chromium.org/chromedriver/downloads
        # metterlo in venv nel percorso qua sotto
        # ho cercato di fare in modo che il percorso che ho messo valesse per tutti,
        # ma potrebbe non funzionare a seconda della struttura del vostro progetto...
        self.selenium = webdriver.Chrome(executable_path=get_chromedriver_path())
        self.user = User.objects.create_user(username="Utente1", password="Admin1")

        # inizializza qui tutto il test database

    # questo metodo chiude il server quando finiscono i test
    def tearDown(self):
        self.selenium.quit()

    def test1RegisterLogin(self):
        selenium = self.selenium

        selenium.get(self.live_server_url + '/')  # apro la pagina root del sito

        try:
            WebDriverWait(selenium, timeout).until(EC.url_contains('login'))
        except TimeoutException:
            print("Timeout all'apertura del sito e redirect a login")

        assert "Login" in selenium.title  # verifico che il redirect da root a login funzioni correttamente
        assert "Username..." in selenium.page_source
        assert "Password..." in selenium.page_source

        # apre la pagina register
        signup_link = selenium.find_element(By.ID, 'signup')
        signup_link.click()
        # selenium.get(self.live_server_url + '/register')   # ho sostituito con la pagina di login e click a register per implementare un test aggiuntivo all'inizio

        # aspetta che gli elementi vengano caricati prima di cercarli, se ci mette più
        # di 5 secondi lancia un'eccezione

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'username')))
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'password1')))
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'password2')))
            WebDriverWait(selenium, timeout).until(EC.element_to_be_clickable((By.ID, 'submit')))
        except TimeoutException:
            print("Page took too long to load!")

        assert 'Registrati' in selenium.title
        assert 'scrumboard' in selenium.page_source

        # cerca gli elementi nella pagina
        username = selenium.find_element(By.NAME, 'username')
        password1 = selenium.find_element(By.NAME, 'password1')
        password2 = selenium.find_element(By.NAME, 'password2')
        submit = selenium.find_element(By.ID, 'submit')

        # inserisce le credenziali
        username.send_keys('Utente2')
        password1.send_keys('Admin2')
        password2.send_keys('Admin2')
        submit.click()

        # aspetta che la pagina cambi
        try:
            WebDriverWait(selenium, timeout).until(EC.url_contains('login'))
        except TimeoutException:
            print("Page took too long to load!")
        assert "Login" in selenium.title
        assert "successo" in selenium.page_source

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'username')))
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'password')))
            WebDriverWait(selenium, timeout).until(EC.element_to_be_clickable((By.ID, 'submit')))
        except TimeoutException:
            print("Page took too long to load!")

        assert 'Login' in selenium.title
        assert 'scrumboard' in selenium.page_source

        username = selenium.find_element(By.ID, 'username')
        password = selenium.find_element(By.ID, 'password')
        submit = selenium.find_element(By.ID, 'submit')

        username.send_keys('Utente2')
        password.send_keys('Admin2')
        submit.click()

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'aggiungi_board')))
        except TimeoutException:
            print("timeout entrata pagina dashboard")

        # controlla che siamo in dashboard

        assert "BOARD" in selenium.page_source
        assert "Le mie board" in selenium.title

        time.sleep(1)

    def test2DashBoard(self):
        selenium = self.selenium
        total_cards = 0
        total_columns = 0
        total_story_points = 0
        total_boards = 0

        selenium.get(self.live_server_url + '/')

        self.login(selenium, timeout)

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'aggiungi_board')))
        except TimeoutException:
            print("timeout entrata pagina dashboard")

        # controlla che siamo in dashboard

        assert "BOARD" in selenium.page_source
        assert "Le mie board" in selenium.title

        add_board = selenium.find_element(By.ID, 'aggiungi_board')
        add_board.click()

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'id_nome')))
        except TimeoutException:
            print("timeout entrata pagina crazione board")

        # controlla che siamo dentro aggiunta board

        assert 'Aggiunta board' in selenium.title

        board_name_input = selenium.find_element(By.ID, 'id_nome')
        submit = selenium.find_element(By.ID, 'submit_new_board')  # stesso di sopra

        new_board_name = "Board 1"
        board_name_input.send_keys(new_board_name)
        total_boards += 1
        # time.sleep(1)
        submit.click()  # aggiungo nuova board

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'board_name')))
        except TimeoutException:
            print("timeout entrata pagina board")

        # controlla che siamo dentro board detail

        assert "Board Detail" in selenium.title  # vado alla nuova board
        assert 'La board è ancora vuota :(' in selenium.page_source
        assert new_board_name in selenium.page_source

        add_column_button = selenium.find_element(By.ID, 'add_column')
        add_column_button.click()  # entro nella pagina di aggiunta colonna

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'submit_new_column')))
        except TimeoutException:
            print("timeout entrata pagina aggiunta colonna")

        # controlla che siamo dentro aggiunta colonna

        assert 'Aggiunta colonna' in selenium.title
        assert 'Nome colonna:' in selenium.page_source

        new_column_name = "Colonna 1"
        submit = selenium.find_element(By.ID, 'submit_new_column')
        new_column_name_input = selenium.find_element(By.ID, 'id_nome')
        new_column_name_input.send_keys(new_column_name)

        # time.sleep(1)
        total_columns += 1
        submit.click()  # invio nuova colonna

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'board_name')))
        except TimeoutException:
            print("timeout ritorno pagina board dopo aggiunta colonna")

        # controlla che siamo tornati dentro board detail con la nuova colonna dentro

        assert "Board Detail" in selenium.title
        assert new_column_name in selenium.page_source

        add_card_button = selenium.find_element(By.ID, 'add_card')
        add_card_button.click()

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'id_descrizione')))
        except TimeoutException:
            print("timeout entrata pagina aggiunta card")

        # controlla che siamo entrati nella pagina di aggiunta card

        assert "Aggiunta card" in selenium.title
        assert "Nome card:" in selenium.page_source

        # preparo card da aggiungere
        new_card_name = "Card 1"
        new_card_description = "Test descrizione card 1"
        new_card_storypoints = 3
        new_card_column = new_column_name

        new_card_name_input = selenium.find_element(By.ID, 'id_nome')
        new_card_description_input = selenium.find_element(By.ID, 'id_descrizione')
        new_card_storypoints_input = selenium.find_element(By.ID, 'id_story_points')
        new_card_column_input = selenium.find_element(By.ID, 'id_colonna')

        # riempio i campi
        new_card_name_input.send_keys(new_card_name)
        new_card_description_input.send_keys(new_card_description)
        new_card_storypoints_input.clear()  # serve per togliere lo 0 iniziale ed evitare che un 3 diventi 30
        new_card_storypoints_input.send_keys(new_card_storypoints)
        new_card_column_input.send_keys(new_card_column)

        submit = selenium.find_element(By.ID, 'submit_new_card')
        submit.click()

        total_cards += 1
        total_story_points += new_card_storypoints

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'board_name')))
        except TimeoutException:
            print("timeout ritorno pagina board dopo aggiunta card")

        # controlla che siamo entrati nella pagina di burndown

        assert "Board Detail" in selenium.title
        assert new_card_name in selenium.page_source
        assert new_card_description in selenium.page_source

        burndown_button = selenium.find_element(By.ID, 'burndown')
        burndown_button.click()

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'burndown_title')))
        except TimeoutException:
            print("timeout entrata pagina burndown")

        storypoints_total_field = int(
            selenium.find_element(By.ID, 'storypoints_total').text)  # prendo gli story points visualizzati nella pagina
        cards_total_field = int(
            selenium.find_element(By.ID, 'cards_total').text)  # prendo le cards visualizzate nella pagina
        back_button = selenium.find_element(By.ID, 'back_button')

        assert "Burndown" in selenium.title
        assert "Burndown" in selenium.page_source
        assert new_board_name in selenium.page_source

        self.assertEqual(storypoints_total_field,
                         total_story_points)  # confronto storypoints visualizzati con quelli sommati qui nei test
        self.assertEqual(cards_total_field, total_cards)  # confronto cards visualizzate con quelle sommate qui nei test

        back_button.click()  # torno indietro a showboard

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'board_name')))
        except TimeoutException:
            print("timeout ritorno pagina board dopo burndown")

        # controlla che siamo tornati dentro board detail dopo burndown

        assert "Board Detail" in selenium.title
        assert new_column_name in selenium.page_source

        edit_card_icon = selenium.find_element(By.ID,
                                               'edit_card_icon_1')  # seleziono la prima card creata, nel caso siano presenti più di una
        edit_card_icon.click()  # entro in modifica card

        # controlla che siamo entrati in modifica card

        assert "Modifica card" in selenium.title
        assert "modifica_card" in selenium.current_url
        assert new_card_name in selenium.page_source
        assert new_card_description in selenium.page_source

        edited_card_name = new_card_name + " edit"
        edited_card_description = new_card_description + " edit"
        edit_card_name_field = selenium.find_element(By.ID, 'id_nome')
        edit_card_description_field = selenium.find_element(By.ID, 'id_descrizione')
        submit = selenium.find_element(By.ID, 'submit_edited_card')

        edit_card_name_field.clear()  # pulisco il campo prima di cambiarlo
        edit_card_description_field.clear()  # pulisco il campo prima di cambiarlo

        edit_card_name_field.send_keys(edited_card_name)
        edit_card_description_field.send_keys(edited_card_description)
        submit.click()

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'board_name')))
        except TimeoutException:
            print("timeout tornando in pagina board da modifica card")

        # controlla che siamo tornati dentro board detail da modifica card

        assert "Board Detail" in selenium.title
        assert new_column_name in selenium.page_source
        assert edited_card_name in selenium.page_source
        assert edited_card_description in selenium.page_source

        column_name_link = selenium.find_element(By.ID,
                                                 'column_name_link_1')  # seleziono la prima colonna creata, nel caso siano presenti più di una
        column_name_link.click()

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'id_nome')))
        except TimeoutException:
            print("timeout entrata pagina modifica colonna")

        # controlla che siamo nella pagina di modifica colonna

        assert "Modifica colonna" in selenium.title
        assert "modifica_colonna" in selenium.current_url
        assert new_column_name in selenium.page_source
        assert edited_card_name in selenium.page_source
        assert edited_card_description in selenium.page_source

        delete_card_icon = selenium.find_element(By.ID,
                                                 'delete_card_icon_1')  # seleziono la prima card creata, nel caso siano presenti più di una
        delete_card_icon.click()  # entro in modifica card
        selenium.switch_to.alert.accept()  # accetto l'ok dall'alert javascript
        total_cards -= 1

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'id_nome')))
        except TimeoutException:
            print("timeout entrata pagina modifica colonna dopo cancellazione card")

        # controlla che siamo nella pagina di modifica colonna

        assert "Modifica colonna" in selenium.title
        assert "modifica_colonna" in selenium.current_url
        assert new_column_name in selenium.page_source
        assert edited_card_name not in selenium.page_source  # card appena cancellata
        assert edited_card_description not in selenium.page_source  # card appena cancellata

        edited_column_name = new_column_name + " edit"
        edit_column_name_field = selenium.find_element(By.ID, 'id_nome')
        submit = selenium.find_element(By.ID, 'submit_edited_column')

        edit_column_name_field.clear()
        edit_column_name_field.send_keys(edited_column_name)

        submit.click()

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'board_name')))
        except TimeoutException:
            print("timeout tornando in pagina board da modifica colonna")

        # controlla che siamo tornati dentro board detail da modifica colonna

        assert "Board Detail" in selenium.title
        assert edited_column_name in selenium.page_source
        assert edited_card_name not in selenium.page_source  # card cancellata prima
        assert edited_card_description not in selenium.page_source  # card cancellata prima

        delete_column_icon = selenium.find_element(By.ID, 'delete_column_icon_1')
        delete_column_icon.click()
        selenium.switch_to.alert.accept()  # accetto l'ok dall'alert javascript

        total_columns -= 1

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'board_name')))
        except TimeoutException:
            print("timeout tornando in pagina board da modifica colonna")

        # controlla che siamo tornati dentro board dopo cancellazione colonna

        assert "Board Detail" in selenium.title
        assert 'La board è ancora vuota :(' in selenium.page_source
        assert edited_column_name not in selenium.page_source
        assert edited_card_name not in selenium.page_source  # card cancellata prima
        assert edited_card_description not in selenium.page_source  # card cancellata prima

        time.sleep(1)

    def test3Logout(self):
        selenium = self.selenium

        selenium.get(self.live_server_url + '/')

        self.login(selenium, timeout)

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'aggiungi_board')))
        except TimeoutException:
            print("timeout entrata pagina dashboard")

        assert "BOARD" in selenium.page_source
        assert "Le mie board" in selenium.title

        logout_button = selenium.find_element(By.ID, 'logout_button')
        logout_button.click()

        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'username')))
        except TimeoutException:
            print("timeout entrata pagina dashboard")

        assert "Login" in selenium.title
        assert "login" in selenium.current_url
        assert "Non hai un account?" in selenium.page_source

        time.sleep(1)

    # metodo per fare il login senza ripetere il codice ogni volta
    def login(self, selenium, timeout):
        try:
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'username')))
            WebDriverWait(selenium, timeout).until(EC.presence_of_element_located((By.ID, 'password')))
            WebDriverWait(selenium, timeout).until(EC.element_to_be_clickable((By.ID, 'submit')))
        except TimeoutException:
            print("Page took too long to load!")

        assert 'Login' in selenium.title
        assert 'scrumboard' in selenium.page_source

        username = selenium.find_element(By.ID, 'username')
        password = selenium.find_element(By.ID, 'password')
        submit = selenium.find_element(By.ID, 'submit')

        username.send_keys('Utente1')
        password.send_keys('Admin1')
        submit.click()


if __name__ == '__main__':
    unittest.main()
