from rest_framework import serializers
from .models import Projekt, Profil, Zespol, Zadanie
from django.contrib.auth.models import User

class ZespolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zespol
        fields = '__all__'

class ProjektSerializer(serializers.ModelSerializer):
    zespoly = ZespolSerializer(many=True, read_only=True)

    class Meta:
        model = Projekt
        fields = '__all__'

    def create(self, validated_data):
        zespoly_data = validated_data.pop('zespoly', [])
        projekt = Projekt.objects.create(**validated_data)

        for zespol_data in zespoly_data:
            zespol, created = Zespol.objects.get_or_create(**zespol_data)
            projekt.zespoly.add(zespol)

        return projekt

    def update(self, instance, validated_data):
        instance.nazwa = validated_data.get('nazwa', instance.nazwa)
        instance.opis = validated_data.get('opis', instance.opis)
        instance.data_rozpoczecia = validated_data.get('data_ropoczecia', instance.data_rozpoczecia)
        instance.termin_wykonania = validated_data.get('termin_wykonania', instance.termin_wykonania)
        instance.status = validated_data.get('status', instance.status)

        zespoly_data = validated_data.get('zespoly', [])
        instance.zespoly.clear()

        for zespol_data in zespoly_data:
            zespol, created = Zespol.objects.get_or_create(**zespol_data)
            instance.zespoly.add(zespol)

        instance.save()
        return instance

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = '__all__'

class ZadanieSerializer(serializers.ModelSerializer):
    przypisany_uzytkownik = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Zadanie
        fields = '__all__'

    def create(self, validated_data):
        return Zadanie.objects.create(**validated_data)


    def update(self, instance, validated_data):
        instance.tytul = validated_data.get('tytul', instance.tytul)
        instance.opis = validated_data.get('opis', instance.opis)
        instance.projekt = validated_data.get('projekt', instance.projekt)
        instance.data_rozpoczecia = validated_data.get('data_rozpoczecia', instance.data_rozpoczecia)
        instance.termin_wykonania = validated_data.get('termin_wykonania', instance.termin_wykonania)
        instance.priorytet = validated_data.get('priorytet', instance.priorytet)
        instance.status = validated_data.get('status', instance.status)
        instance.przypisany_uzytkownik = validated_data.get('przypisany_uzytkownik', instance.przypisany_uzytkownik)
        instance.save()
        return instance

class ZadanieAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zadanie
        fields = ['status']



