from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms
from django.contrib import messages
from datetime import datetime

# ===== FORM =====
class RezervaceForm(forms.ModelForm):
    class Meta:
        model = Vypujcka
        fields = ["auto", "datum_od", "datum_do"]


# ===== REGISTRACE ZÁKAZNÍKA =====
def registrace_zakaznik(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            Zakaznik.objects.create(
                user=user,
                jmeno=user.username,
                prijmeni="",
                telefon=""
            )

            return redirect("login_zakaznik")

    else:
        form = UserCreationForm()

        # 🔥 PLACEHOLDERY
        form.fields['username'].widget.attrs.update({
            'placeholder': 'Uživatelské jméno'
        })

        form.fields['password1'].widget.attrs.update({
            'placeholder': 'Heslo'
        })

        form.fields['password2'].widget.attrs.update({
            'placeholder': 'Potvrzení hesla'
        })

    return render(request, "core/registrace.html", {"form": form})


# ===== LOGIN ZÁKAZNÍK =====
def login_zakaznik(request):
    if request.user.is_authenticated:
        if Zakaznik.objects.filter(user=request.user).exists():
            return redirect("auta")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            if Zakaznik.objects.filter(user=user).exists():
                login(request, user)
                return redirect("auta")  
        else:
            return render(request, "core/login_zakaznik.html", {"error": "Neplatné údaje"})

    return render(request, "core/login_zakaznik.html")


# ===== LOGIN ZAMĚSTNANEC =====
def login_zamestnanec(request):
    if request.user.is_authenticated:
       if Zamestnanec.objects.filter(user=request.user).exists():
            return redirect("sprava")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            if Zamestnanec.objects.filter(user=user).exists():
                login(request, user)
                return redirect("sprava")  
        else:
            return render(request, "core/login_zakaznik.html", {"error": "Neplatné údaje"})

    return render(request, "core/login_zamestnanec.html")


# ===== VOZOVÝ PARK =====
@login_required
def seznam_aut(request):
    auta = Auto.objects.all()
    return render(request, "core/auta.html", {"auta": auta})


# ===== REZERVACE =====
@login_required
def rezervace(request):
    zakaznik = Zakaznik.objects.get(user=request.user)

    auto_id = request.GET.get("auto_id")

    if request.method == "POST":
        form = RezervaceForm(request.POST)
        if form.is_valid():
            vypujcka = form.save(commit=False)
            vypujcka.zakaznik = zakaznik
            vypujcka.save()
            return redirect("auta")
    else:
        form = RezervaceForm()

        # 🔥 předvyplnění auta
        if auto_id:
            form.fields["auto"].initial = auto_id

    return render(request, "core/rezervace.html", {"form": form})


# ===== SPRÁVA =====
@login_required
def sprava_vypujcek(request):
    if not Zamestnanec.objects.filter(user=request.user).exists():
        return redirect("/")

    vypujcky = Vypujcka.objects.all()
    return render(request, "core/sprava.html", {"vypujcky": vypujcky})


# ===== SCHVÁLENÍ =====
@login_required
def schvalit(request, id):
    zam = Zamestnanec.objects.get(user=request.user)

    v = Vypujcka.objects.get(id=id)
    v.stav = "schvaleno"
    v.zamestnanec = zam
    v.save()

    return redirect("sprava")

def vyber_login(request):
    return render(request, "core/vyber_login.html")

