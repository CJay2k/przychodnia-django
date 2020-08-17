from django.test import SimpleTestCase
from django.urls import reverse, resolve

from lekarze.views import lekarze_delete_view_list, lekarze_delete_view, lekarze_list_view, lekarze_create_view
from przychodnia_lekarska.views import GeneratePDF, konto, deactivate
from wizyty.views import wizyty_odwolaj_view, wizyty_oczekujace_view, wizyty_dodaj_view, wizyty_dodaj2_view, \
    wizyty_odwolaj_view_list, wizyty_historia_view, wizyty_zarzadzaj_view_list, wizyty_zarzadzaj_view


class TestUrls(SimpleTestCase):
    def test_lekarze_list_view(self):
        url = reverse('lekarze_list')
        self.assertEquals(resolve(url).func, lekarze_list_view)

    def test_lekarze_create_view(self):
        url = reverse('lekarze_create')
        self.assertEquals(resolve(url).func, lekarze_create_view)

    def test_lekarze_delete_view_list(self):
        url = reverse('lekarze_delete_list')
        self.assertEquals(resolve(url).func, lekarze_delete_view_list)

    def test_wizyty_list_view(self):
        url = reverse('wizyty_oczekujace')
        self.assertEquals(resolve(url).func, wizyty_oczekujace_view)

    def test_wizyty_delete_view(self):
        url = reverse('wyzyty_dodaj1')
        self.assertEquals(resolve(url).func, wizyty_dodaj_view)

    def test_wizyty_odwolaj_view_list(self):
        url = reverse('wizyty_odwolaj_list')
        self.assertEquals(resolve(url).func, wizyty_odwolaj_view_list)

    def test_wizyty_historia_view(self):
        url = reverse('wizyty_historia')
        self.assertEquals(resolve(url).func, wizyty_historia_view)

    def test_wizyty_zarzadzaj_view_list(self):
        url = reverse('wizyty_zarzadzaj_list')
        self.assertEquals(resolve(url).func, wizyty_zarzadzaj_view_list)

    def test_konto_view(self):
        url = reverse('konto')
        self.assertEquals(resolve(url).func, konto)

    def test_deactivate(self):
        url = reverse('deactivate')
        self.assertEquals(resolve(url).func, deactivate)
