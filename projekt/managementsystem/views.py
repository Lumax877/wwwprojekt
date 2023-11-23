from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Projekt, Zadanie, Zespol, Profil
from .serializers import ProjektSerializer, ZadanieSerializer, ZespolSerializer, ProfilSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

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
        serializer.save()

class ZadanieDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zadanie.objects.all()
    serializer_class = ZadanieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

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

