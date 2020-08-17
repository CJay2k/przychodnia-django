![HOME](https://raw.githubusercontent.com/CJay2k/przychodnia-django/master/dokumentacja/home.png)
**![Kliknij aby zobaczyć więcej screenów](https://github.com/CJay2k/przychodnia-django/tree/master/dokumentacja)**

# 1. Opis Systemu
Celem projektu było wykonanie aplikacji webowej, która będzie zawierała samą stronę internetową jak i bazę danych. 

Dzięki aplikacji pacjent, będzie w stanie umówić się na wizytę do danego specjalisty. Będzie to możliwe dzięki rozbudowanemu systemowi, który obejmuje możliwość rezerwacji wizyt u najlepszych specjalistów od poniedziałku do piątku. 

Strona posiada przewagę nad lokalnymi przychodniami, gdyż nie potrzebuje zewnętrznej ingerencji człowieka przy rezerwowaniu godzin, a co za tym idzie, jest szybsza, wydajniejsza  i przede wszystkim działa 24/7. 

Pomostem łączącym interfejs użytkownika z bazą jest Python wraz z Django i SQL Lite. Wygląd tejże strony jest możliwy dzięki zastosowaniu języka CSS ora biblioteki Bootstrap, która ułatwia pracę od strony graficznej. 

Projekt uwzględnił też użycie języka JavaScript do wyświetlania slajdów na jednej z naszych podstron. Za obsługę rezerwacji wizyt jest odpowiedzialny Django. Dzięki zastosowaniu tejże technologi jest możliwa walidacja z poziomu systemu oraz wysyłanie danych do Bazy. 

W projekcie znajdziemy pliki Pythonowskie z rozszerzeniem (.py), pliki odpowiadające za styl (.css), JavaScript (.js), HTML 5 (.html) czy też obrazki (.jpeg). Plik odpowiadający za bazę danych naszego systemu posiada rozszerzenie (.sqlite3). Strona jest oczywiście w pełni responsywna 

# 2. Elementy Strony
Strona naszej przychodni lekarskiej zbudowana jest na elementach blokowych „div”. 

Strona główna jak i wszystkie podstrony posiadają Menu górne- na które składają się (HOME, AKTUALNOŚCI, KONTAKT, REJESTRACJA ORAZ LOGOWANIE). 

W przypadku zalogowanych użytkowników Menu zawiera (HOME, AKTUALNOŚCI, KONTAKT, WIZYTY I IMIĘ PACJENTA).

W stopce Umieszczone zostały trzy ikonki: Facebook, Twitter oraz GitHub, które umożliwiają szybkie przejście do podanych stron. 

Strona posiada margines z prawej jak i lewej strony. Natomiast centralne logo  wypełnia w pełni obszar roboczy naszej przeglądarki. 

Nasza przychodnia posiada łącznie 8 podstron, z czego 5 jest dostępnych bez uprzedniego logowania, jest to: 
* Home (Logo i wiadomości), 
* Aktualności (informacje), 
* Kontakt (formularz do kontaktu), 
* Rejestracja (formularz umożliwiający rejestracje),
* Logowanie. Po zalogowaniu mamy też możliwość wejścia w zakładkę wizyty (formularz rezerwacji wizyty). 

A w przypadku zalogowanego Admina: 
* Raporty, 
* Lekarze (dodawanie Lekarza), 
* Panel Administracyjny.
   
## 1. Home
Strona główna zbudowana jest z menu górnego, Centralnego Logo wraz z nazwą naszej przychodni lekarskiej oraz stopką.  Na stronie głównej zostały zawarte informacje o naszej placówce wraz z aktualnościami, które każdy pacjent chciałby mieć pod ręką.

## 2. Kontakt
Podstrona odpowiedzialna za kontakt z naszą placówką, wyposażona jest w formularz zgłoszeniowy w centralnej części aplikacji. 

Formularz został podzielony na cztery części, gdzie po kolei wpisujemy:
* Imię i Nazwisko, 
* E-mail, 
* Telefon Kontaktowy,
* Treść naszej wiadomości. 

Pod wszystkim możemy zobaczyć niebieski przycisk wyślij, który zatwierdza całą operację.

## 3. Rejestracja
Jest to podstrona odpowiedzialna za rejestrację użytkownika w systemie, poprzez dodanie jego danych do wcześniej zbudowanej bazy danych. 

W tymże formularzu znajdziemy pola: 
* Nazwa użytkownika, 
* E-mail, 
* Imię, 
* Nazwisko, 
* Hasło, 
* Ponowne okienko wprowadzenia hasła. 

Na samym dole możemy znaleźć przycisk morskiego kolory Zarejestruj.

## 4. Logowanie
W tej części aplikacji znajdziemy formularz logowania się do systemu. 

Jeżeli nie posiadamy jeszcze konta, będziemy mogli przejść do formularza rejestracji przy pomocy przycisku.

Formularz składa się z dwóch pól:
* Nazwa Użytkownika
* Hasło. 

Jest też pole Pamiętaj Mnie, które pozwoli na niewylogowywanie się z danej sesji użytkownika na dłuższy czas. Wszystko zakończone jest przyciskiem ZALOGUJ.

## 5. Wizyty

Jest to najważniejsza część naszej aplikacji, w której możemy zobaczyć rejestrację do lekarza.
Jest ona podzielona na cztery części: 
* Lista Wizyt, 
* Dodaj Wizytę, 
* Przełóż Wizytę, 
* Odwołaj Wizytę.

Pola te mają morski przyjemny kolor, by każdy pacjent czuł się jak u siebie w domu. 
Sam formularz rejestracji na wizytę zawiera pola: 
* Data, 
* Godzina,
* Opis.

## 6. Lekarze

Ta podstrona jest dostępna tylko i wyłącznie dla administratora sieci. Znajdziemy tam trzy pola: 
* Listę Lekarzy, 
* Dodaj Lekarza,
* Usuń Lekarza.
