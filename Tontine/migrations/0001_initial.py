# Generated by Django 3.2.9 on 2022-01-15 13:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poste_canidat', models.CharField(choices=[('President', 'President'), ('Tresorier', 'Tresorier'), ('Secretaire', 'Secretaire'), ('Secretaire Adjoint', 'Secretaire Adjoint'), ('Commissaire aux Compte', 'Commissaire aux Compte'), ('Commissaire aux Compte Adjoint', 'Commissaire aux Compte Adjoint')], max_length=40, verbose_name='Post Candidature')),
                ('nombre_de_voix', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['nombre_de_voix'],
            },
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateField(verbose_name="Date De L'election")),
                ('terme', models.CharField(blank=True, max_length=3000, verbose_name='Terme Election')),
                ('temp_renouvelable', models.CharField(max_length=200, verbose_name='Temp Renouvelable')),
                ('date_creation', models.DateTimeField(auto_now=True)),
                ('date_fin_canditure', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=40)),
                ('surname', models.CharField(max_length=40)),
                ('address', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email  address')),
                ('telephone', models.CharField(max_length=40, verbose_name='Telephone Number')),
                ('date_of_birth', models.DateField()),
                ('profession', models.CharField(max_length=50)),
                ('profile', models.ImageField(blank=True, default='profile.png', null=True, upload_to='')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('candidat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Tontine.candidat')),
                ('election', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.election')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tontine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom Tontine')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date De Creation')),
                ('slogan', models.CharField(max_length=255, verbose_name='Slogan')),
                ('reglement_interieur', models.TextField(verbose_name='R??glement Int??rieur')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reunion',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('nom', models.CharField(max_length=50, verbose_name='Nom De Reunion')),
                ('date', models.DateField(verbose_name='Date Reunion')),
                ('lieu', models.CharField(max_length=40, verbose_name='Lieux Reunion')),
                ('heure', models.TimeField(verbose_name='Heure Reunion')),
                ('motif', models.TextField(max_length=500, verbose_name='Motif reunion')),
                ('id_tontine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.tontine')),
            ],
        ),
        migrations.CreateModel(
            name='Rapport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rapport', models.TextField(verbose_name='Rapport De La Reunion')),
                ('reunion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.reunion')),
            ],
        ),
        migrations.CreateModel(
            name='Pret',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('nom_pret', models.CharField(max_length=255, verbose_name='Nom')),
                ('date', models.DateField()),
                ('montant', models.IntegerField()),
                ('raison', models.CharField(max_length=255, verbose_name='Raison Du Pret')),
                ('data_de_paiement_reel', models.DateField(verbose_name='Date de paiement r??el')),
                ('taux_interet', models.FloatField(verbose_name="Taux D'interet")),
                ('taux_de_sanction', models.FloatField(verbose_name='Taux de sanction')),
                ('id_tontine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.tontine')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('reunion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.reunion')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField(verbose_name='Message')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('link', models.CharField(blank=True, max_length=100000, verbose_name='lien')),
                ('demande', models.BooleanField(default=False)),
                ('type_n', models.CharField(blank=True, choices=[('D', 'D'), ('A', 'A')], max_length=2)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usern', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='MesTontine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_part', models.IntegerField(verbose_name='Nombre de part')),
                ('fonction', models.CharField(blank=True, choices=[('PR', 'President'), ('TR', 'Tresorier'), ('SC', 'Secretaire'), ('SCA', 'Secretaire Adjoint'), ('CAC', 'Commissaire aux Compte'), ('CACA', 'Commissaire aux Compte Adjoint')], max_length=30)),
                ('date_integration', models.DateTimeField(default=datetime.datetime.now)),
                ('id_membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membres', to=settings.AUTH_USER_MODEL)),
                ('id_tontine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tontine', to='Tontine.tontine')),
            ],
        ),
        migrations.CreateModel(
            name='MesReunion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poste', models.CharField(blank=True, choices=[('PR', 'President'), ('TR', 'Tresorier'), ('SC', 'Secretaire'), ('SCA', 'Secretaire Adjoint'), ('CAC', 'Commissaire aux Compte'), ('CACA', 'Commissaire aux Compte Adjoint')], max_length=40)),
                ('membre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reunion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.reunion')),
            ],
        ),
        migrations.CreateModel(
            name='Fond',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('type_fond', models.CharField(max_length=30, verbose_name='Type De Fond')),
                ('nom', models.CharField(max_length=30, verbose_name='Nom')),
                ('regles', models.CharField(max_length=255, verbose_name='R??gles')),
                ('montant_base', models.FloatField(verbose_name='Montant De Base')),
                ('objectif', models.TextField(verbose_name='Objectif')),
                ('id_tontine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.tontine')),
            ],
        ),
        migrations.AddField(
            model_name='election',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='election',
            name='id_tontine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.tontine'),
        ),
        migrations.CreateModel(
            name='Cotisation',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('nom_cotisation', models.CharField(max_length=60, verbose_name='Nom')),
                ('montant', models.FloatField(verbose_name='Montant Cotisation')),
                ('date', models.DateField(verbose_name='Date de d??but')),
                ('cycle', models.IntegerField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('nombre_participant', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_tontine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tontine.tontine')),
            ],
        ),
        migrations.AddField(
            model_name='candidat',
            name='id_election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='election', to='Tontine.election'),
        ),
        migrations.AddField(
            model_name='candidat',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
