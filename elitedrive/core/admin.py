from django.contrib import admin
from .models import Auto, Zamestnanec, Zakaznik, Vypujcka

admin.site.register(Auto)
admin.site.register(Zamestnanec)
admin.site.register(Zakaznik)
admin.site.register(Vypujcka)