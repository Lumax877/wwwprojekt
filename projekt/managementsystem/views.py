from rest_framework import generics, permissions
from .models import Projekt, Zadanie, Zespol, Profil
from .serializers import ProjektSerializer, ZadanieSerializer, ZespolSerializer, ProfilSerializer, ZadanieAssignedSerializer
from .permissions import IsAdminOrReadOnly, CanChangeAssignedTaskPermission
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.exceptions import PermissionDenied

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Projekt.objects.all()
        else:
            zadania_uzytkownika = Zadanie.objects.filter(przypisany_uzytkownik=user)
            id_projektow = zadania_uzytkownika.values_list('projekt', flat=True).distinct()
            return Projekt.objects.filter(id__in=id_projektow)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Tylko administratorzy mogą tworzyć nowe projekty.")
        serializer.save()

class ProjektDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Projekt.objects.all()
    serializer_class = ProjektSerializer
    permission_classes = [IsAdminOrReadOnly]

class ZadanieListCreateView(generics.ListCreateAPIView):
    queryset = Zadanie.objects.all()
    serializer_class = ZadanieSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(przypisany_uzytkownik=self.request.user)

class ZadanieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zadanie.objects.all()
    serializer_class = ZadanieSerializer
    permission_classes = [IsAdminOrReadOnly]

class ZadanieChangeStatus(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ZadanieAssignedSerializer
    permission_classes = [CanChangeAssignedTaskPermission]

    def get_queryset(self):
        return Zadanie.objects.filter(przypisany_uzytkownik=self.request.user)

class ZespolListCreateView(generics.ListCreateAPIView):
    queryset = Zespol.objects.all()
    serializer_class = ZespolSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Tylko administratorzy mogą tworzyć nowe zespoły.")
        serializer.save()

class ZespolDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zespol.objects.all()
    serializer_class = ZespolSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProfilListCreateView(generics.ListCreateAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Tylko administratorzy mogą przydzielać użytkowników do zespołów.")
        serializer.save()

class ProfilDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer
    permission_classes = [IsAdminOrReadOnly]

class PrzypiszZadanieUzytkownikowiView(generics.RetrieveUpdateAPIView):
    queryset = Zadanie.objects.all()
    serializer_class = ZadanieSerializer
    permission_classes = [permissions.IsAuthenticated] # IsAdminOrReadOnly?

    def perform_update(self, serializer):
        username = self.request.data.get('przypisany_uzytkownik')

        try:
            user = User.objects.get(id=username) #XD
        except User.DoesNotExist:
            raise Http404("User not found.")
        serializer.save(przypisany_uzytkownik=user)

class PobierzPrzypisaneZadaniaUzytkownikaView(generics.ListAPIView):
    serializer_class = ZadanieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Zadanie.objects.filter(przypisany_uzytkownik=self.request.user)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

