from django.urls import path
from .views import *

from django.contrib.auth.views import LogoutView

urlpatterns = [
    # hlavní stránka
    path("", seznam_aut, name="auta"),

    # zákazník
    path("rezervace/", rezervace, name="rezervace"),
    path("registrace/", registrace_zakaznik, name="registrace"),
    path("login-zakaznik/", login_zakaznik, name="login_zakaznik"),
   
    # zaměstnanec
    path("login-zamestnanec/", login_zamestnanec, name="login_zamestnanec"),
    path("sprava/", sprava_vypujcek, name="sprava"),
    path("schvalit/<int:id>/", schvalit, name="schvalit"),
    path("logout/", LogoutView.as_view(next_page="/vyber-login/"), name="logout"),
    path("vyber-login/", vyber_login, name="vyber_login"),
]