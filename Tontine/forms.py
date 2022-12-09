from typing import Any, Dict
from django.core import validators
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms import ModelForm
from django.forms.widgets import SelectDateWidget
from .models import Tontine, Reunion, Candidat, Election, Fond, Cotisation
from django import forms
from django.db import models


class TontineCreationForm(ModelForm):

    reglement_interieur = forms.Textarea()

    class Meta:
        model = Tontine
        fields = ['nom', 'slogan', 'reglement_interieur']

    widgets = {
        'nom': forms.TextInput(attrs={'class': 'form-control'}),
        'slogan': forms.TextInput(attrs={'class': 'form-control'}),
        'reglement_interieur': forms.TextInput(attrs={'class': 'form-control'}),
    }

    def clean_field(self):
        data = self.cleaned_data.get("reglement_interieur")

        if len(data) == 1:
            raise ValidationError("Reglement Interieur Non Valide")

        return data


class ReunionCreationForm(ModelForm):

    class Meta:
        model = Reunion
        fields = '__all__'
        #fields = ['tontine', 'nom', 'date', 'motif', 'lieu', 'heure']


class CreateReunion(ModelForm):

    class Meta:
        model = Reunion
        fields = ['nom', 'date', 'motif', 'lieu', 'heure']


class CreateElection(ModelForm):
    terme = forms.CharField(
        max_length=3000, help_text='  Veillez entrez un bon terme svp!')

    class Meta:
        model = Election
        fields = ['date', 'terme', 'temp_renouvelable', 'date_fin_canditure']

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get("date")
        data1 = cleaned_data.get("date_fin_canditure")

        print(type(data), type(data1))

        if data1 > data:
            msg = [
                'La date de fin de candidature doit etre inferieur a la date de election!']
            raise ValidationError(msg)

    def save(self, commit: bool = False):
        elect = super().save(commit=commit)
        if commit:
            elect.save()
        return elect

    # def cleaned_date_fin_candidature(self):
    #     date = self.cleaned_data.get('date_fin_candidature')
    #     date1 = self.cleaned_data.get("temp_renouvelable")
    #     if date > date1:
    #         raise ValidationError(
    #             "La Date De Fin de Candidature doit etre inferieur a la date de l'ection!")

    #     return date


class DeposerCandidature(ModelForm):

    PRES = 'President'  # president
    TRE = 'Tresorier'  # tresorier
    SC = 'Secretaire'  # secraitaire
    CAC = 'Commissaire aux Compte'  # commissaire au compte

    choice = [
        (PRES, PRES),
        (TRE, TRE),
        (SC, SC),
        (CAC, CAC)
    ]

    poste_canidat = forms.ChoiceField(
        choices=choice, help_text='Selectionner le poste au qu\'elle vous soliciter ')

    class Meta:
        model = Candidat
        fields = ['poste_canidat']


class CreateFond(ModelForm):

    class Meta:
        model = Fond
        fields = ['type_fond', 'nom', 'regles', 'montant_base', 'objectif']


class CreateCotisation(ModelForm):

    class Meta:
        model = Cotisation
        fields = '__all__'
        exclude = ['id_tontine', 'nombre_participant', 'creator', 'cycle']
