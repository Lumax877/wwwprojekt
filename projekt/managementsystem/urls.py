from django.urls import path
from .views import home, CustomLoginView, CustomLogoutView, AdminLoginView, admin_home
from .views import (
    ProjektListCreateView, ProjektDetailView,
    ZadanieListCreateView, ZadanieDetailView,
    ZespolListCreateView, ZespolDetailView,
    ProfilListCreateView, ProfilDetailView,
    PrzypiszZadanieUzytkownikowiView, PobierzPrzypisaneZadaniaUzytkownikaView,
    register, ZadanieChangeStatus
)

urlpatterns = [
    path('projekty/', ProjektListCreateView.as_view(), name='projekt-list-create'),
    path('projekty/<int:pk>/', ProjektDetailView.as_view(), name='projekt-detail'),

    path('zadania/', ZadanieListCreateView.as_view(), name='zadanie-list-create'),
    path('zadania/<int:pk>/', ZadanieDetailView.as_view(), name='zadanie-detail'),

    path('zespoly/', ZespolListCreateView.as_view(), name='zespol-list-create'),
    path('zespoly/<int:pk>/', ZespolDetailView.as_view(), name='zespol-detail'),

    path('profile/', ProfilListCreateView.as_view(), name='profil-list-create'),
    path('profile/<int:pk>/', ProfilDetailView.as_view(), name='profil-detail'),

    path('przypisz-zadanie/<int:pk>', PrzypiszZadanieUzytkownikowiView.as_view(), name='przypisz-zadanie'),
    path('moje-zadania/', PobierzPrzypisaneZadaniaUzytkownikaView.as_view(), name='moje-zadania'),
    path('zmien-status/<int:pk>', ZadanieChangeStatus.as_view(), name='zmien-status'),

    path('home/', home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/home/', admin_home, name='admin-home'),

    path('register/', register, name='register'),
]
