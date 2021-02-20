from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



TITLE_CHOICES = (
    ('SZUKAM', 'Szukam'),
    ('ZNALEZIONO', 'Znaleziono'),
    ('ZAKOŃCZONE', 'Zakończone'),
    ('INNE', 'Inne'),
)

ACCEPT_CHOICES = (
    ('TAK', 'Tak'),
    ('NIE', 'Nie'),
)

class ToDo(models.Model):
    Miasto = models.CharField(max_length=25, help_text='Podać miasto')
    Lokalizacja = models.CharField(max_length=50, blank=True, help_text='<b>* Pole niewymagane</b><br>Podać lokalizację(np. ulica)')
    Opis = models.TextField(help_text='Podaj dokładny opis') #jezeli nie chce to nie musi uzupelniac
    Zdjęcie = models.ImageField(upload_to='index/pictures', blank=True, help_text='<b>* Pole niewymagane</b><br>Wklej zdjęcie')
    created=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Kategoria = models.CharField(max_length=15, choices=TITLE_CHOICES, help_text='Wybierz kategorie ogłoszenia')
    Kontakt = models.CharField(max_length=30, blank=True, help_text='<b>* Pole niewymagane</b><br>Numer kontaktowy, mail itp.')
    Akceptacja = models.CharField(max_length=15, choices=ACCEPT_CHOICES, blank=True)
    def __str__(self):
        return self.user.username
