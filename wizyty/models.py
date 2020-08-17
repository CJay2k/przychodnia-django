from datetime import date, time

from django.contrib.auth.models import User as Pacjenci
from django.db import models
from django.db.models import Model

from lekarze.models import Lekarze

STATUS = [
    ('Ocz', 'Oczekująca'),
    ('Odw', 'Odwołana'),
    ('Zak', 'Zakończona'),
]

GODZINY_LISTA = ((time(8, 00), '08:00'),
                 (time(8, 15), '08:15'),
                 (time(8, 30), '08:30'),
                 (time(8, 45), '08:45'),
                 (time(9, 00), '09:00'),
                 (time(9, 15), '09:15'),
                 (time(9, 30), '09:30'),
                 (time(9, 45), '09:45'),
                 (time(10, 00), '10:00'),
                 (time(10, 15), '10:15'),
                 (time(10, 30), '10:30'),
                 (time(10, 45), '10:45'),
                 (time(11, 00), '11:00'),
                 (time(11, 15), '11:15'),
                 (time(11, 30), '11:30'),
                 (time(11, 45), '11:45'),
                 (time(12, 00), '12:00'),
                 (time(12, 15), '12:15'),
                 (time(12, 30), '12:30'),
                 (time(12, 45), '12:45'),
                 (time(13, 00), '13:00'),
                 (time(13, 15), '13:15'),
                 (time(13, 30), '13:30'),
                 (time(13, 45), '13:45'),
                 (time(14, 00), '14:00'),
                 (time(14, 15), '14:15'),
                 (time(14, 30), '14:30'),
                 (time(14, 45), '14:45'),
                 (time(15, 00), '15:00'),
                 (time(15, 15), '15:15'),
                 (time(15, 30), '15:30'),
                 (time(15, 45), '15:45'))

GODZINY = ['08:00', '08:15', '08:30', '08:45',
           '09:00', '09:15', '09:30', '09:45',
           '10:00', '10:15', '10:30', '10:45',
           '11:00', '11:15', '11:30', '11:45',
           '12:00', '12:15', '12:30', '12:45',
           '13:00', '13:15', '13:30', '13:45',
           '14:00', '14:15', '14:30', '14:45',
           '15:00', '15:15', '15:30', '15:45'
           ]


def czy_godzina_poprawna(godzina):
    try:
        if len(godzina) > 5:
            godzina = str(godzina)[:-3]
        time.fromisoformat(godzina)
        if godzina in GODZINY:
            return True
    except ValueError:
        print("Podana godzina jest niepoprawna. Oczekiwana godzina w formacie HH:MM lub HH:MM:SS")
        return False
    print("Podana godzina jest niepoprawna. Oczekiwana godzina w formacie HH:MM lub HH:MM:SS")
    return False


def czy_data_poprawna(data):
    try:
        if date.fromisoformat(data) > date.today():
            return True
    except ValueError:
        print("Podana data jest niepoprawna. Oczekiwana data w formacie YYYY-MM-DD")
        return False
    except TypeError:
        print("Podana data jest niepoprawna. Oczekiwana data w formacie YYYY-MM-DD")
        return False
    print("Podana data jest z przeszłości")
    return False


def czy_termin_wolny(lekarz, data, godzina):
    for termin in lekarz.terminy:
        if data == termin.data and godzina == termin.godzina and termin.status == 'Oczekująca':
            print(f"Termin {data} {godzina} jest już zajęty!")

            return False
    return True


def przeloz_wizyte(lekarz, wizyta, nowa_data, nowa_godzina):
    if czy_data_poprawna(nowa_data) and czy_godzina_poprawna(nowa_godzina) and czy_termin_wolny(lekarz, nowa_data,
                                                                                                nowa_godzina):
        print(f"Pomyślnie zmnieniono datę wizyty z {wizyta.data} {wizyta.godzina} na {nowa_data} {nowa_godzina}")
        wizyta.data = nowa_data
        wizyta.godzina = nowa_godzina


def aktualizuj_status(wizyta, status):
    if wizyta is not None:
        if wizyta.status == 'Oczekująca':
            if status == "Zakończona":
                wizyta.status = status
                print("Wizyta zostałą pomyślnie 'Zakończona'")
            elif status == "Odwołana":
                wizyta.status = status
                print("Wizyta została pomyślnie 'Odwołana'")
            else:
                print("Nie udało się zaktualizować statusu wizyty. Podano błędny status.")
        else:
            print("Można zaktualizować tylko wizyty ze statusem 'Oczekująca'")
    else:
        print("Taka wizyta nie istnieje!")


def nowa_wizyta(pacjent, lekarz, opis, data, godzina, front=False):
    nowa_wizyta = None

    if czy_data_poprawna(data) and czy_godzina_poprawna(godzina):
        nowa_wizyta = Wizyty.objects.create(pacjent=pacjent, lekarz=lekarz, opis=opis, data=data, godzina=godzina)

        if not front:
            if czy_termin_wolny(lekarz, data, godzina):
                lekarz.terminy.append(nowa_wizyta)
                nowa_wizyta.save()
                return nowa_wizyta
        else:
            nowa_wizyta.save()
            return nowa_wizyta

    if nowa_wizyta:
        nowa_wizyta.delete()
    return nowa_wizyta


class Wizyty(models.Model):
    pacjent = models.ForeignKey(Pacjenci, on_delete=models.CASCADE)
    lekarz = models.ForeignKey(Lekarze, on_delete=models.CASCADE)
    opis = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField()
    godzina = models.TimeField(choices=GODZINY_LISTA)
    status = models.CharField(choices=STATUS, default='Oczekująca', max_length=20)
    recepta = models.CharField(max_length=200, blank=True, null=True)
