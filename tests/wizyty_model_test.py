from django.contrib.auth.models import User as Pacjenci, Group
from django.test import TestCase

from lekarze.models import Lekarze, dodaj_lekarza
from wizyty.models import aktualizuj_status, przeloz_wizyte, nowa_wizyta


class UzytkownicyTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(UzytkownicyTestCase, cls).setUpClass()
        Group.objects.get_or_create(name='pacjent')
        Group.objects.get_or_create(name='lekarz')

        cls.uz = Pacjenci.objects.create_user(username="lekasz", password="avadakedavra", first_name="lord",
                                                   last_name="voldemort")
        cls.lekarz = dodaj_lekarza(cls.uz, "czarna magia", 666)

        cls.pacjent = Pacjenci.objects.create_user(username="qwerttsadzcsa", password="testtest", first_name="Janusz",
                                                   last_name="Tracz")

    def setUp(self):
        super(UzytkownicyTestCase, self).setUp()
        self.lekarz.terminy.clear()

    def test_nowa_wizyta_poprawne_dane(self):
        print("Rozpoczęcie testu dodawania nowej wizyty dla poprawnych danych.")

        wizyta = nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-03-16", "08:30")

        self.assertEqual(wizyta.status, "Oczekująca")
        self.assertEqual(wizyta.pacjent, self.pacjent)
        self.assertEqual(wizyta.lekarz, self.lekarz)
        self.assertEqual(wizyta.data, "2020-03-16")

        print("-------------------------------------------------------------------------------------------------------")

    def test_nowa_wizyta_na_ten_sam_termin(self):
        print("Rozpoczęcie testu dodawania wizyt na ten sam termin.")

        self.lekarz.lista_zajetych_terminow()
        nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-12-26", "09:30")
        self.lekarz.lista_zajetych_terminow()
        nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-12-27", "09:30")
        self.lekarz.lista_zajetych_terminow()
        nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-12-27", "09:30")
        self.lekarz.lista_zajetych_terminow()
        nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-12-27", "11:30")
        self.lekarz.lista_zajetych_terminow()
        nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-12-27", "11:30")
        self.lekarz.lista_zajetych_terminow()
        print(self.lekarz.terminy)
        self.lekarz.lista_wolnych_terminow("2020-12-27")

        self.assertEqual(len(self.lekarz.terminy), 3)
        print("-------------------------------------------------------------------------------------------------------")

    def test_nowa_wizyta_bledny_format_daty(self):
        print("Rozpoczęcie testu dodawania nowej wizyty dla błędnego formatu daty.")

        wizyta = nowa_wizyta(self.pacjent, self.lekarz, "test", "17-12-2020", "08:30")
        self.assertEqual(wizyta, None)

        print("-------------------------------------------------------------------------------------------------------")

    def test_nowa_wizyta_bledna_data(self):
        print("Rozpoczęcie testu dodawania nowej wizyty dla błędnej daty.")

        wizyta = nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-13-33", "08:30")
        self.assertEqual(wizyta, None)

        print("-------------------------------------------------------------------------------------------------------")

    def test_nowa_wizyta_bledny_format_godziny(self):
        print("Rozpoczęcie testu dodawania nowej wizyty dla błędnego formatu godziny.")

        wizyta = nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-11-05", "8:30")
        self.assertEqual(wizyta, None)

        print("-------------------------------------------------------------------------------------------------------")

    def test_aktualizuj_status_poprawne_dane(self):
        print("Rozpoczęcie testu aktualizacji statusu wizyty dla poprawnych danych.")

        print(self.lekarz.terminy)
        wizyta1 = nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-11-01", "08:30")
        print(self.lekarz.terminy)
        nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-11-01", "08:30")
        print(self.lekarz.terminy)

        aktualizuj_status(wizyta1, "Odwołana")

        nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-11-01", "08:30")
        print(self.lekarz.terminy)

        self.assertEquals(wizyta1.status, "Odwołana")

        print("-------------------------------------------------------------------------------------------------------")

    def test_aktualizuj_status_bledne_dane(self):
        print("Rozpoczęcie testu aktualizacji statusu wizyty dla niepoprawnych danych.")

        wizyta = nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-07-05", "08:30")
        aktualizuj_status(wizyta, "nowy_błędny_status")

        self.assertNotEqual(wizyta.status, "nowy_błędny_status")

        print("-------------------------------------------------------------------------------------------------------")

    def test_przeloz_wizyte_poprawne_dane(self):
        print("Rozpoczęcie testu przełożenia daty wizyty dla poprawnych danych.")

        wizyta = nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-11-05", "08:30")
        przeloz_wizyte(self.lekarz, wizyta, "2020-12-27", "09:45")

        self.assertEqual(wizyta.data, "2020-12-27")
        self.assertEqual(wizyta.godzina, "09:45")

        print("-------------------------------------------------------------------------------------------------------")

    def test_przeloz_wizyte_bledne_dane(self):
        print("Rozpoczęcie testu przełożenia daty wizyty dla niepoprawnych danych.")

        wizyta = nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-01-05", "08:30")
        przeloz_wizyte(self.lekarz, wizyta, "2019-12-37", "08:30")

        self.assertNotEqual(wizyta, "2019-12-37", "08:30")

        print("-------------------------------------------------------------------------------------------------------")

    def test_przeloz_wizyte_data_wczesniejsza_niz_aktualna(self):
        print("Rozpoczęcie testu przełożenia daty wizyty dla daty z przeszłości.")

        wizyta = nowa_wizyta(self.pacjent, self.lekarz, "test", "2020-11-05", "08:30")
        przeloz_wizyte(self.lekarz, wizyta, "2019-11-27", "08:30")

        self.assertNotEqual(wizyta.data, "2019-11-27", "08:30")

        print("-------------------------------------------------------------------------------------------------------")
