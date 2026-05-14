from django.db import models
from django.contrib.auth.models import User


class Auto(models.Model):
    model = models.CharField(max_length=100)
    spz = models.CharField(max_length=20)
    denni_sazba = models.DecimalField(max_digits=10, decimal_places=2)
    stav_nadrze = models.IntegerField()
    obrazek = models.ImageField(upload_to='auta/', blank=True, null=True)

    def __str__(self):
        return self.model


class Zakaznik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    jmeno = models.CharField(max_length=50)
    prijmeni = models.CharField(max_length=50)
    telefon = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"


class Zamestnanec(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    jmeno = models.CharField(max_length=50)
    prijmeni = models.CharField(max_length=50)
    pozice = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"


class Vypujcka(models.Model):
    STAVY = [
        ("cekajici", "Čeká"),
        ("schvaleno", "Schváleno"),
    ]

    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    zakaznik = models.ForeignKey(Zakaznik, on_delete=models.CASCADE)
    zamestnanec = models.ForeignKey(Zamestnanec, on_delete=models.SET_NULL, null=True, blank=True)

    datum_od = models.DateField()
    datum_do = models.DateField()
    stav = models.CharField(max_length=20, choices=STAVY, default="cekajici")
    celkova_cena = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.auto} - {self.zakaznik}"