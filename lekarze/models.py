from datetime import date
from django.core.validators import MinValueValidator

from django.contrib.auth.models import User, Group

from django.db import models


GODZINY = ['08:00', '08:15', '08:30', '08:45',
           '09:00', '09:15', '09:30', '09:45',
           '10:00', '10:15', '10:30', '10:45',
           '11:00', '11:15', '11:30', '11:45',
           '12:00', '12:15', '12:30', '12:45',
           '13:00', '13:15', '13:30', '13:45',
           '14:00', '14:15', '14:30', '14:45',
           '15:00', '15:15', '15:30', '15:45'
           ]


def czy_data_poprawna(data):
    try:
        if date.fromisoformat(data) > date.today():
            return True
    except ValueError:
        print("Podana data jest niepoprawna. Oczekiwana data w formacie YYYY-MM-DD")
        return False
    except TypeError:
        print("Podana data jest niepoprawna")
        return False
    print("Podana data jest z przeszłości")
    return False


def dodaj_lekarza(uzytkownik, specjalizacja, numer_gabinetu):
    nowy_lekarz = None

    if uzytkownik and len(specjalizacja) >= 1 and int(numer_gabinetu) >= 1:
        nowy_lekarz = Lekarze.objects.create(uzytkownik=uzytkownik, specjalizacja=specjalizacja, numer_gabinetu=numer_gabinetu)

        nowy_lekarz.save()

        my_group = Group.objects.get(name='lekarz')
        my_group.user_set.add(uzytkownik)

        my_group = Group.objects.get(name='pacjent')
        my_group.user_set.remove(uzytkownik)

    return nowy_lekarz


def usun_lekarza(lekarz):

    for wizyta in lekarz.terminy:
        if wizyta.status == 'Oczekująca':
            wizyta.status = "Odwołana"

    lekarz.aktywny = False


class Lekarze(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    specjalizacja = models.CharField(max_length=25)
    numer_gabinetu = models.IntegerField(validators=[MinValueValidator(1)])
    terminy = []
    aktywny = models.BooleanField(default=True)

    def to_string(self):
        return f"{self.uzytkownik}, {self.specjalizacja}, {self.numer_gabinetu}"

    def lista_zajetych_terminow(self):
        self.terminy.sort(key=lambda x: x.data)
        for rekord in self.terminy:
            print(f"{rekord.pacjent}, {rekord.lekarz}, {rekord.opis}, {rekord.data}, {rekord.godzina}, {rekord.status}")
        print()

    def lista_wolnych_terminow(self, data):
        if czy_data_poprawna(data):
            wolne_godziny = GODZINY.copy()
            for rekord in self.terminy:
                if rekord.data == data and rekord.godzina in wolne_godziny:
                    wolne_godziny.remove(rekord.godzina)

            print(wolne_godziny)
            return wolne_godziny

