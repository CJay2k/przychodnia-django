from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from wizyty.models import Wizyty
from .forms import LekarzeForm
from .models import Lekarze, dodaj_lekarza, usun_lekarza


@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name='#')
def lekarze_list_view(request):
    queryset = Lekarze.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "lista_lekarzy.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name='#')
def lekarze_create_view(request):
    wiadomosc = ''

    if request.method == 'POST':
        form = LekarzeForm(request.POST or None)
        if form.is_valid():
            nowy_uzytkownik = User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password1'), first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))

            dodaj_lekarza(nowy_uzytkownik, request.POST.get('specjalizacja'), request.POST.get('numer_gabinetu'))
            wiadomosc = '<h4 style="color: green">Pomyślnie dodano nowego lekarza</h4>'
    else:
        form = LekarzeForm()

    context = {
        'form': form,
        "wiadomosc": wiadomosc,
    }
    return render(request, "dodaj_lekarza.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name='#')
def lekarze_delete_view(request, pk):
    if request.method == 'POST':
        obj = Lekarze.objects.get(pk=pk)

        usun_lekarza(obj)

        for rekord in Wizyty.objects.all():
            if rekord.status == 'Oczekująca':
                rekord.status = "Odwołana"
                rekord.save()

        obj.aktywny = False

        obj.uzytkownik.is_active = False
        obj.uzytkownik.save()
        obj.save()

    return redirect('lekarze_delete_list')


@login_required
@user_passes_test(lambda u: u.is_superuser, redirect_field_name='#')
def lekarze_delete_view_list(request):
    wiadomosc = ''

    queryset = Lekarze.objects.all()
    context = {
        "object_list": queryset,
        "wiadomosc": wiadomosc,
    }
    return render(request, "usun_lekarzy.html", context)
