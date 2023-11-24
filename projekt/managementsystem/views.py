from rest_framework import generics, permissions
from .models import Projekt, Zadanie, Zespol, Profil
from .serializers import ProjektSerializer, ZadanieSerializer, ZespolSerializer, ProfilSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test

def home(request):
    if request.user.is_authenticated:
        zadania = Zadanie.objects.filter(przypisany_uzytkownik=request.user)
        return render(request, 'home.html', {'zadania': zadania})
    else:
        return redirect('login')

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home'

class AdminLoginView(LoginView):
    template_name = 'admin_login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.user.is_staff:
            return redirect('admin-home')
        return response

@user_passes_test(lambda u: u.is_staff)
def admin_home(request):
    return render(request, 'admin_home.html')

class ProjektListCreateView(generics.ListCreateAPIView):
    queryset = Projekt.objects.all()
    serializer_class = ProjektSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProjektDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projekt.objects.all()
    serializer_class = ProjektSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

class ZadanieListCreateView(generics.ListCreateAPIView):
    queryset = Zadanie.objects.all()
    serializer_class = ZadanieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(przypisany_uzytkownik=self.request.user)

class ZadanieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zadanie.objects.all()
    serializer_class = ZadanieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] #IsOwnerOrReadOnly not working

class ZespolListCreateView(generics.ListCreateAPIView):
    queryset = Zespol.objects.all()
    serializer_class = ZespolSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ZespolDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zespol.objects.all()
    serializer_class = ZespolSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProfilListCreateView(generics.ListCreateAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProfilDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class PrzypiszZadanieUzytkownikowiView(generics.UpdateAPIView):
    queryset = Zadanie.objects.all()
    serializer_class = ZadanieSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(przypisany_uzytkownik=self.request.user)

class PobierzPrzypisaneZadaniaUzytkownikaView(generics.ListAPIView):
    serializer_class = ZadanieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Zadanie.objects.filter(przypisany_uzytkownik=self.request.user)

