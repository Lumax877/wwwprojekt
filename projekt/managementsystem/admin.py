from django.contrib import admin
from .models import Zespol, Projekt, Zadanie, Profil

admin.site.register(Zespol)
admin.site.register(Profil)

class ZadanieAdmin(admin.ModelAdmin):
    list_display = ["tytul", "projekt", "priorytet", "status"]
    list_filter = ('projekt', 'priorytet', 'status')

class ProjektAdmin(admin.ModelAdmin):
    list_display = ["nazwa", "data_rozpoczecia", "termin_wykonania", "status"]
    list_filter = ('termin_wykonania', 'nazwa', 'status')

admin.site.register(Projekt, ProjektAdmin)
admin.site.register(Zadanie, ZadanieAdmin)

# Register your models here.
