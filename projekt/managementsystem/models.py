from django.db import models
from django.contrib.auth.models import User

class Zespol(models.Model):
    nazwa = models.CharField(max_length=100)
    czlonkowie = models.ManyToManyField(User)
    data_utworzenia = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nazwa

class Projekt(models.Model):
    nazwa = models.CharField(max_length=100)
    opis = models.TextField()
    data_rozpoczecia = models.DateField()
    termin_wykonania = models.DateField()
    status = models.CharField(max_length=50, choices=[('W trakcie', 'W trakcie'), ('Zakończony', 'Zakończony')])

    def __str__(self):
        return self.nazwa

class Zadanie(models.Model):
    tytul = models.CharField(max_length=100)
    opis = models.TextField()
    projekt = models.ForeignKey(Projekt, on_delete=models.CASCADE, related_name='zadania')
    data_rozpoczecia = models.DateField()
    termin_wykonania = models.DateField()
    priorytet = models.CharField(max_length=50, choices=[('Wysoki', 'Wysoki'), ('Średni', 'Średni'), ('Niski', 'Niski')])
    status = models.CharField(max_length=50, choices=[('Nowe', 'Nowe'), ('W trakcie', 'W trakcie'), ('Zakońcozne', 'Zakończone')])
    przypisany_uzytkownik = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.tytul

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    zespoly = models.ManyToManyField(Zespol, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def przypisane_zadania(self):
        return Zadanie.objects.filter(przypisany_uzytkownik=self.user)

