import datetime
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from django.contrib.auth.models import User

import uuid

from django.db.models.base import Model
from django.db.models.expressions import F, Func

# Create your models here.

# 3UPDATING THE USER FORMS


class MyUserManager(BaseUserManager):

    def create_user(self, username, surname, address, email, telephone, date_of_birth, profession, profile, password=None):
        if not username:
            raise ValueError("User muts have a user username")
        if not surname:
            raise ValueError("User muts have a user surname")
        if not address:
            raise ValueError("User muts have a user address")
        if not email:
            raise ValueError("User muts have a user email")
        if not telephone:
            raise ValueError("User muts have a user telephone")
        if not date_of_birth:
            raise ValueError("User muts have a user date of birth")
        if not profession:
            raise ValueError("User muts have a user profession")

        user = self.model(
            username=username,
            surname=surname,
            address=address,
            email=self.normalize_email(email),
            telephone=telephone,
            date_of_birth=date_of_birth,
            profession=profession,
            profile=profile
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, surname, address, email, telephone, date_of_birth, profession, profile, password=None):

        user = self.create_user(
            username,
            surname,
            address,
            email,
            telephone,
            date_of_birth,
            profession,
            profile,
            password=password
        )

        user.is_admin = True
        user.save(using=self._db)

        return user


class MyUser(AbstractBaseUser):

    username = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    email = models.EmailField(
        verbose_name='email  address', max_length=255, unique=True)
    telephone = models.CharField('Telephone Number', max_length=40)
    date_of_birth = models.DateField()
    profession = models.CharField(max_length=50)
    profile = models.ImageField(default="profile.png", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'username',
        'surname',
        'address',
        'telephone',
        'date_of_birth',
        'profession',
        'profile'
    ]

    def __str__(self):
        return self.username + " "+self.surname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def imageURL(self):
        try:
            img = self.profile.url
            #print("image ", img)
        except:
            img = ''

        return img

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


User = MyUser

# Table Tontine


class Tontine(models.Model):
    nom = models.CharField('Nom Tontine', max_length=255)
    date_creation = models.DateTimeField('Date De Creation', auto_now_add=True)
    #numero_de_membre = models.IntegerField('Nombre De Membre',default=1)
    slogan = models.CharField('Slogan', max_length=255)
    reglement_interieur = models.TextField('Réglement Intérieur')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nom)

# Table TontineMembre


class MesTontine(models.Model):
    PRES = 'PR'  # president
    TRE = 'TR'  # tresorier
    SC = 'SC'  # secraitaire
    SCA = 'SCA'  # secretaire adjoint
    CAC = 'CAC'  # commissaire au compte
    CACA = 'CACA'  # commissaire au compte adjoint
    FONCTION = [
        (PRES, 'President'),
        (TRE, 'Tresorier'),
        (SC, 'Secretaire'),
        (SCA, 'Secretaire Adjoint'),
        (CAC, 'Commissaire aux Compte'),
        (CACA, 'Commissaire aux Compte Adjoint')
    ]
    id_tontine = models.ForeignKey(
        Tontine, on_delete=models.CASCADE, related_name='tontine')
    id_membre = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='membres')
    nombre_de_part = models.IntegerField('Nombre de part')
    fonction = models.CharField(max_length=30, choices=FONCTION, blank=True)
    date_integration = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return 'Tontine : {} Membre : {}'.format(self.id_tontine, self.id_membre)


# TABLE ELECTION
class Election(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    date = models.DateField("Date De L'election")
    id_tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE)
    terme = models.CharField("Terme Election", max_length=3000, blank=True)
    temp_renouvelable = models.CharField('Temp Renouvelable', max_length=200)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_creation = models.DateTimeField(auto_now=True)
    date_fin_canditure = models.DateField()

    class Meta:
        ordering = ['date']

    def __str__(self):
        return 'Election {} Du {}'.format(self.id_tontine, self.date)

# Table Candidat


class Candidat(models.Model):
    PRES = 'President'  # president
    TRE = 'Tresorier'  # tresorier
    SC = 'Secretaire'  # secraitaire
    SCA = 'Secretaire Adjoint'  # secretaire adjoint
    CAC = 'Commissaire aux Compte'  # commissaire au compte
    CACA = 'Commissaire aux Compte Adjoint'  # commissaire au compte adjoint
    POST = [
        (PRES, 'President'),
        (TRE, 'Tresorier'),
        (SC, 'Secretaire'),
        (SCA, 'Secretaire Adjoint'),
        (CAC, 'Commissaire aux Compte'),
        (CACA, 'Commissaire aux Compte Adjoint')
    ]
    id_election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="election")
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    poste_canidat = models.CharField(
        'Post Candidature', choices=POST, max_length=40)
    nombre_de_voix = models.IntegerField(default=0)
    # liste_participant = models.ManyToManyField(User,blank=True) #liste de ceux qui on voter

    class Meta:
        ordering = ['-nombre_de_voix']

    def __str__(self):
        return f'{self.id_user}'

# table cotisation


class Cotisation(models.Model):

    cycle_cotisation = (
        ('journalier', 'journalier'),
        ('Hebdomaider', 'Hebdomaider'),
        ('Menseule', 'Menseule'),
        ('Trimestriel', 'Trimestriel'),
        ('Semestriel', 'Semestriel'),
        ('Annuelle', 'Annuelle')
    )

    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    id_tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE)
    nom_cotisation = models.CharField('Nom', max_length=60)
    montant = models.FloatField('Montant Cotisation')
    date = models.DateField('Date de début')
    cycle = models.CharField(
        max_length=40, choices=cycle_cotisation, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    nombre_participant = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    #paticipant = models.ManyToManyField(User, blank=True)

# table pret


class Pret(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    id_tontine = models.ForeignKey(Tontine, models.CASCADE)
    nom_pret = models.CharField('Nom', max_length=255)
    date = models.DateField()
    member = models.ForeignKey(User, models.DO_NOTHING)
    montant = models.IntegerField()
    raison = models.CharField('Raison Du Pret', max_length=255)
    data_de_paiement_reel = models.DateField('Date de paiement réel')
    taux_interet = models.FloatField("Taux D'interet")
    taux_de_sanction = models.FloatField("Taux de sanction")


# table fond
class Fond(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    id_tontine = models.ForeignKey(Tontine, on_delete=models.CASCADE)
    type_fond = models.CharField('Type De Fond', max_length=30)
    nom = models.CharField('Nom', max_length=30)
    regles = models.CharField('Régles', max_length=255)
    montant_base = models.FloatField('Montant De Base')
    objectif = models.TextField("Objectif")

    def __str__(self):
        return f'Fond {self.nom} Tontine {self.id_tontine}'

# table reunion


class Reunion(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)
    id_tontine = models.ForeignKey(
        Tontine, on_delete=models.CASCADE)
    nom = models.CharField("Nom De Reunion", max_length=50)
    date = models.DateField('Date Reunion')
    lieu = models.CharField('Lieux Reunion', max_length=40)
    heure = models.TimeField('Heure Reunion')
    motif = models.TextField('Motif reunion', max_length=500)

    def __str__(self):
        return self.nom


class MesReunion(models.Model):
    PRES = 'PR'  # president
    TRE = 'TR'  # tresorier
    SC = 'SC'  # secraitaire
    SCA = 'SCA'  # secretaire adjoint
    CAC = 'CAC'  # commissaire au compte
    CACA = 'CACA'  # commissaire au compte adjoint
    FONCTION = [
        (PRES, 'President'),
        (TRE, 'Tresorier'),
        (SC, 'Secretaire'),
        (SCA, 'Secretaire Adjoint'),
        (CAC, 'Commissaire aux Compte'),
        (CACA, 'Commissaire aux Compte Adjoint')
    ]
    membre = models.ForeignKey(User, models.CASCADE)
    reunion = models.ForeignKey(Reunion, models.CASCADE)
    poste = models.CharField(choices=FONCTION, max_length=40, blank=True)


class Rapport(models.Model):
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)
    rapport = models.TextField("Rapport De La Reunion")

    def __str__(self):
        return f'Reunion : {self.reunion} Rapport: {self.rapport}'


class Participe(models.Model):
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)
    membre = models.ForeignKey(User, models.DO_NOTHING)


class Notification(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='usern')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    msg = models.TextField("Message")
    date = models.DateTimeField(
        auto_now_add=True)
    link = models.CharField('lien', blank=True, max_length=100000)
    demande = models.BooleanField(default=False)
    choix = (
        ('D', 'D'),
        ('A', 'A')
    )
    type_n = models.CharField(max_length=2, choices=choix, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Message {self.msg}  par {self.sender}"


class Vote(models.Model):
    member = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidat = models.ForeignKey(Candidat, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.member} Vote {self.candidat} Pour {self.election}'
