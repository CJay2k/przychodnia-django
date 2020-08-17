import datetime

from django.contrib.auth.models import User as Pacjenci
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test


from lekarze.models import Lekarze, czy_data_poprawna
from wizyty.models import nowa_wizyta, aktualizuj_status
from .forms import WizytyForm
from .models import Wizyty


@login_required
@user_passes_test(lambda u: u.groups.filter(name='pacjent').exists() or u.groups.filter(name='lekarz').exists() or u.is_superuser, redirect_field_name='#')
def wizyty_oczekujace_view(request):
    wiadomosc = "<h4>Brak zaplanowanych wizyt</h4>"
    queryset = Wizyty.objects.all()
    context = {
        "object_list": queryset,
        "wiadomosc": wiadomosc,
    }
    return render(request, "oczekujace_wizyty.html", context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='pacjent').exists(), redirect_field_name='#')
def wizyty_dodaj_view(request):
    queryset = Lekarze.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "dodaj_wizyte.html", context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='pacjent').exists(), redirect_field_name='#')
def wizyty_dodaj2_view(request, pk):
    wiadomosc = "<br>"
    wolne_godziny = ""
    wyswietl = True
    if request.method == 'POST':
        form = WizytyForm(request.POST or None)
        if form.is_valid():
            godz = request.POST.get('godzina')
            if len(godz) > 5:
                godz = str(request.POST.get('godzina'))[:-3]
            if not Wizyty.objects.filter(lekarz=Lekarze.objects.get(id=pk), data=request.POST.get('data'), godzina=godz, status='Oczekująca'):
                nowa_wizyta(Pacjenci.objects.get(id=request.user.id),
                            Lekarze.objects.get(id=pk), request.POST.get('opis'),
                            request.POST.get('data'),
                            request.POST.get('godzina'), front=True)
                wiadomosc = '<h4 style="color: green">Nowa wizyta została pomyślnie utworzona!</h4>'
                wyswietl = False
                if not czy_data_poprawna(request.POST.get('data')):
                    wiadomosc = '<h4 style="color: darkred">Wizyta może zostać umówiona na dzień jutrzejszy lub później!</h4>'
            else:
                wiadomosc = f'<h4 style="color: darkred">Wybrany termin jest już zajęty!</h4>'

                wolne_godziny = ['08:00', '08:15', '08:30', '08:45',
                                 '09:00', '09:15', '09:30', '09:45',
                                 '10:00', '10:15', '10:30', '10:45',
                                 '11:00', '11:15', '11:30', '11:45',
                                 '12:00', '12:15', '12:30', '12:45',
                                 '13:00', '13:15', '13:30', '13:45',
                                 '14:00', '14:15', '14:30', '14:45',
                                 '15:00', '15:15', '15:30', '15:45'
                                 ]
                for rekord in Wizyty.objects.all():
                    if str(rekord.data) == request.POST.get('data') and str(rekord.godzina)[:-3] in wolne_godziny:
                        wolne_godziny.remove(str(rekord.godzina)[:-3])
    else:
        form = WizytyForm()

    lekarz_object = Lekarze.objects.get(id=pk)
    context = {
        'form': form,
        "wiadomosc": wiadomosc,
        "wolne_godziny": wolne_godziny,
        "wyswietl": wyswietl,
        "lekarz_object": lekarz_object,
    }
    return render(request, "dodaj_wizyte2.html", context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='pacjent').exists() or u.groups.filter(name='lekarz').exists() or u.is_superuser, redirect_field_name='#')
def wizyty_odwolaj_view(request, pk):
    if request.method == 'POST':
        obj = Wizyty.objects.get(pk=pk)

        aktualizuj_status(obj, "Odwołana")
        obj.save()
    return redirect('wizyty_odwolaj_list')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='pacjent').exists() or u.groups.filter(name='lekarz').exists() or u.is_superuser, redirect_field_name='#')
def wizyty_odwolaj_view_list(request):
    wiadomosc = "<h4>Brak oczekujących wizyt</h4>"

    queryset = Wizyty.objects.all()
    context = {
        "object_list": queryset,
        "wiadomosc": wiadomosc,
    }
    return render(request, "odwolaj_wizyte.html", context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='lekarz').exists(), redirect_field_name='#')
def wizyty_zarzadzaj_view(request, pk):
    obj = None
    if request.method == 'POST':
        obj = Wizyty.objects.get(pk=pk)

        if request.POST.get('recepta'):
            obj.recepta = request.POST.get('recepta')
            aktualizuj_status(obj, "Zakończona")
            obj.save()

    return render(request, "zarzadzaj_wizytami2.html", {"obj": obj})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='lekarz').exists(), redirect_field_name='#')
def wizyty_zarzadzaj_view_list(request):
    wiadomosc = "<h4>Brak oczekujących wizyt</h4>"

    queryset = Wizyty.objects.all()
    context = {
        "object_list": queryset,
        "wiadomosc": wiadomosc,
    }
    return render(request, "zarzadzaj_wizytami.html", context)
# # @login_required
# # @user_passes_test(lambda u: u.groups.filter(name='pacjent').exists(), redirect_field_name='#')
# def wizyty_przeloz_view(request, pk):
#     if request.method == 'POST':
#         obj = Wizyty.objects.get(pk=pk)
#
#         aktualizuj_status(obj, "Odwołana")
#         obj.save()
#     return redirect('wizyty_odwolaj_list')
#
#
# def wizyty_przeloz_view_list(request):
#     wiadomosc = "<h4>Brak oczekujących wizyt</h4>"
#
#     queryset = Wizyty.objects.all()
#     context = {
#         "object_list": queryset,
#         "wiadomosc": wiadomosc,
#     }
#     return render(request, "przeloz_wizyte.html", context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='pacjent').exists() or u.groups.filter(name='lekarz').exists() or u.is_superuser, redirect_field_name='#')
def wizyty_historia_view(request):
    wiadomosc = "<h4>Brak wizyt w historii</h4>"

    queryset = Wizyty.objects.all()
    context = {
        "object_list": queryset,
        "wiadomosc": wiadomosc,
    }
    return render(request, "historia_wizyt.html", context)
