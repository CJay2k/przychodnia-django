"""przychodnia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from lekarze.views import lekarze_create_view, lekarze_list_view, lekarze_delete_view, lekarze_delete_view_list
from przychodnia_lekarska.views import index, konto, deactivate, GeneratePDF
from wizyty.views import wizyty_oczekujace_view, wizyty_odwolaj_view, \
    wizyty_dodaj_view, wizyty_odwolaj_view_list, wizyty_historia_view, \
    wizyty_dodaj2_view, wizyty_zarzadzaj_view, wizyty_zarzadzaj_view_list

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),

    path('', index, name='index'),

    path('lekarze/wyswietl', lekarze_list_view, name='lekarze_list'),

    path('lekarze/dodaj', lekarze_create_view, name='lekarze_create'),

    path('lekarze/usun', lekarze_delete_view_list, name='lekarze_delete_list'),
    path('lekarze/usun/<int:pk>/', lekarze_delete_view, name='lekarze_delete'),

    path('wizyty/oczekujace', wizyty_oczekujace_view, name='wizyty_oczekujace'),

    path('wizyty/dodaj', wizyty_dodaj_view, name='wyzyty_dodaj1'),
    path('wizyty/dodaj/<int:pk>/', wizyty_dodaj2_view, name='wyzyty_dodaj2'),

    path('wizyty/odwolaj', wizyty_odwolaj_view_list, name='wizyty_odwolaj_list'),
    path('wizyty/odwolaj/<int:pk>/', wizyty_odwolaj_view, name='wizyty_odwolaj'),

    # path('wizyty/przeloz', wizyty_przeloz_view_list, name='wizyty_przeloz_list'),
    # path('wizyty/przeloz/<int:pk>/', wizyty_przeloz_view, name='wizyty_przeloz'),
    path('wizyty/historia', wizyty_historia_view, name='wizyty_historia'),

    path('wizyty/generuj_raport', GeneratePDF.as_view(), name='generate_pdf'),

    path('wizyty/zarzadzaj', wizyty_zarzadzaj_view_list, name='wizyty_zarzadzaj_list'),
    path('wizyty/zarzadzaj/<int:pk>/', wizyty_zarzadzaj_view, name='wizyty_zarzadzaj'),

    path('konto', konto, name='konto'),
    path('accounts/deactivate', deactivate, name='deactivate'),
]

urlpatterns += staticfiles_urlpatterns()
