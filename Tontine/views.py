import time
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.http import request, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.db import connection, connections
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
from .admin import UserCreationForm, UserChangeForm

from django.contrib import messages
# Create your views here.

from .models import (Candidat, Cotisation, Election, Fond, MesReunion,
                     MesTontine, Notification, Reunion, Tontine, MyUser, Vote)

from .forms import (CreateCotisation, CreateElection, DeposerCandidature,
                    TontineCreationForm, ReunionCreationForm, CreateReunion, CreateFond)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    desc = cursor.description

    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def home(request):

    template = 'tontine/home.html'
    context = {}

    if request.user.is_authenticated:

        mes_association = MesTontine.objects.filter(
            Q(id_membre=request.user.id))

        number_of_tontine_created = Tontine.objects.filter(
            creator=request.user).count()

        context['nb'] = len(mes_association)
        context['association'] = mes_association
        context['number'] = number_of_tontine_created

        return render(request, template, context)
    else:
        return redirect('login')


def create_reunion(request):
    template = 'tontine/create_reunion.html'
    context = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            reunion = ReunionCreationForm(request.POST or None)
            if reunion.is_valid():
                reunion.save()
                return redirect('mes_reunion')
    tontine = ReunionCreationForm

    context['form'] = tontine

    return render(request, template, context)


def create_tontine(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TontineCreationForm(request.POST or None)
            if form.is_valid():
                tontine = form.save(commit=False)
                # id = tontine.id
                tontine.creator = request.user

                mes = MesTontine(id_tontine=tontine,
                                 id_membre=request.user, nombre_de_part=1)

                tontine.save()
                mes.save()

                return redirect('home')

    template = 'tontine/create_tontine.html'
    context = {}

    tontine = TontineCreationForm

    context['form'] = tontine

    return render(request, template, context)


def mes_tontine(request, id):
    template = 'tontine/mes_tontine.html'
    context = {}
    print("===============================================")

    cursor = connection.cursor()
    sql = '''
        SELECT User.id,username,surname,nom FROM
        Tontine_myuser User,Tontine_mestontine,Tontine_tontine
        WHERE User.id = Tontine_mestontine.id_membre_id and  Tontine_mestontine.id_tontine_id = Tontine_tontine.id
        and User.id = {}
    '''.format(id)

    cursor.execute(sql)

    result = dictfetchall(cursor)

    print(connection.queries)

    context['result'] = result

    return render(request, template, context)


def mes_reunion(request):
    template = 'tontine/mes_reunion.html'
    context = {}
    print("===============================================")

    users = MyUser.objects.all()
    print(users)
    l = []

    for u in users:
        meston = MesReunion.objects.filter(membre=u.id)
        l.append(meston)
        # print(u.id," : ",u.username)
        # l.append(meston)
        # for m in meston:print(m.id_tontine.nom)

    # context['result'] = l

    context['result'] = l

    return render(request, template, context)

# AFFICHIER LE PROFILE D'UN MEMEBRE


def profile(request, id):

    template = 'tontine/profile.html'
    context = {}

    user = MyUser.objects.get(id=id)

    context['profile'] = user

    return render(request, template, context)

# CREATION DE REUNION


def create_meeting(request, idtontine):

    template = 'tontine/create_meeting.html'
    context = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            meeting = CreateReunion(request.POST or None)
            if meeting.is_valid():
                tont = Tontine.objects.get(id=idtontine)
                form = meeting.save(commit=False)
                idtontine = request.POST['idtontine']
                form.id_tontine = tont
                name = form.nom
                form.save()
                messages.success(
                    request, (f"Reunion {name} Creer avec Success"))
                return redirect('tontines')
            else:
                messages.warning(
                    request, ("An Error Occur In Creating The Meeting make sure the date has the format YYYY:MM:DD"))
        else:
            meeting = CreateReunion
            context['idtontine'] = idtontine
            context['name'] = Tontine.objects.get(id=idtontine)
            context['form'] = meeting

            return render(request, template, context)
    else:
        return redirect('login')

# AFFICHIER LES DIFFERENTE REUNION D"UNE ASSOCIATION


def list_reunion(request, id):
    template = 'tontine/reunion_tontine.html'
    return

# AFFICHIER LE MEMBRE QUI ON PARTICIPER A UN REUNION


def membre_reunion(request, id):
    template = 'tontine/mes_tontine.html'
    context = {}

    cursor = connection.cursor()
    sql = '''
        SELECT username,surname,nom FROM
        Tontine_myuser,Tontine_mesreunion,Tontine_reunion
        WHERE Tontine_myuser.id = Tontine_mesreunion.id_membre_id and  Tontine_reunion.id = {}
    '''.format(id)

    cursor.execute(sql)

    result = dictfetchall(cursor)

    print(connection.queries)

    return render(request, template, context)

# AFFICHIER LES DETAILS D'UNE TONTINE


def tontine(request, id):

    template = 'tontine/tontine.html'
    context = {}

    sql = '''
        SELECT Tontine_tontine.id,Tontine_tontine.nom,Tontine_tontine.slogan,Tontine_tontine.reglement_interieur,Tontine_tontine.creator,count(*) as `nombre de membre `
        FROM Tontine_tontine,Tontine_mestontine,Tontine_myuser
        WHERE Tontine_tontine.id = Tontine_mestontine.id_tontine_id
        and Tontine_mestontine.id_membre_id = Tontine_myuser.id
        and Tontine_tontine.id = {}
    '''.format(id)

    sql = '''
        SELECT *,count(*) as `nombre de membre `
        FROM Tontine_tontine,Tontine_mestontine,Tontine_myuser
        WHERE Tontine_tontine.id = Tontine_mestontine.id_tontine_id
        and Tontine_mestontine.id_membre_id = Tontine_myuser.id
        and Tontine_tontine.id = {}
    '''.format(id)

    cursor = connection.cursor()
    cursor.execute(sql)

    result = dictfetchall(cursor)
    context['result'] = result[0]

    sql1 = '''
            SELECT Tontine_myuser.id,Tontine_myuser.username,Tontine_myuser.surname,Tontine_myuser.email,Tontine_myuser.telephone,Tontine_myuser.profession,Tontine_mestontine.date_integration FROM Tontine_myuser,Tontine_mestontine,Tontine_tontine
            WHERE Tontine_myuser.id = Tontine_mestontine.id_membre_id and Tontine_mestontine.id_tontine_id = Tontine_tontine.id and Tontine_tontine.id = {}'''.format(id)

    cursor.execute(sql1)

    membre = dictfetchall(cursor)

    context['membre'] = membre
    context['nombre'] = len(membre)

    cotisation = Cotisation.objects.filter(id_tontine=id)

    context['cotisation'] = cotisation

    fond = Fond.objects.filter(id_tontine=id)

    context['fond'] = fond

    y, m, s = time.strftime("%Y-%m-%d").split('-')
    election = Election.objects.filter(Q(id_tontine=id)
                                       & Q(date__gte=datetime.date(int(y), int(m), int(s))
                                           ))

    context['election'] = election
    election = Election.objects.filter(
        Q(id_tontine=id) & Q(date_fin_canditure__lte=datetime.date(int(y), int(m), int(s))))
    candidature = Candidat.objects.filter(
        Q(id_election__in=election) & Q(id_user=request.user.id))

    context['candidature'] = candidature

    return render(request, template, context)

# AFFICHE TOUS LES DIFFERENTE TONTINE


def info_tontine(request):
    if request.user.is_authenticated:

        template = 'tontine/info_tontine.html'
        context = {}

        tontine = Tontine.objects.all()

        cursor = connection.cursor()

        ids = [_.id for _ in tontine]

        id = request.user.id

        l = []

        for _id in ids:

            sql1 = '''
            SELECT Tontine_myuser.id FROM Tontine_myuser,Tontine_mestontine,Tontine_tontine
            WHERE Tontine_myuser.id = Tontine_mestontine.id_membre_id
            and Tontine_mestontine.id_tontine_id = {} and Tontine_myuser.id = {}'''.format(_id, id)

            cursor.execute(sql1)

            membre = cursor.fetchone()

            print(membre)

            l.append(membre)
            x = []
        for _ in l:
            if _:
                x.append(int('{}'.format(_[0])))
            else:
                x += [None]

        li = []

        for (i, t) in enumerate(tontine):
            k = {'id': t.id, 'nom': t.nom, 'slogan': t.slogan, 'date_creation': t.date_creation,
                 'reglement_interieur': t.reglement_interieur, 'u': x[i]}
            li.append(k)

        context['tontines'] = li

        context['username'] = l
        context['test'] = x
        return render(request, template, context)
    else:
        return redirect('login')


def info_reunion(request):
    template = 'tontine/info_reunion.html'
    context = {}

    reunion = Reunion.objects.all()

    context['reunions'] = reunion

    return render(request, template, context)

# CREATION D'UNE ELECTION


def create_election(request, idtontine):
    template = 'tontine/creer_election.html'
    context = {}

    if request.user.is_authenticated:
        if request.method == 'POST':
            election = CreateElection(request.POST or None)
            # elec = election.save(commit=False)
            # if elec.date < datetime.datetime.date():
            #     messages.warning(
            #         request, ("The Date Of the election must be greater than the now"))
            #     return redirect('creer_election/{}/'.format(idtontine))
            if election.is_valid():
                elec = election.save(commit=False)

                y, m, s = time.strftime("%Y-%m-%d").split('-')
                ancient = Election.objects.filter(Q(id_tontine=idtontine) & Q(
                    date=datetime.date(int(y), int(m), int(s))) & Q(terme=elec.terme) & Q(temp_renouvelable=elec.temp_renouvelable) & Q(date_fin_canditure=elec.date_fin_canditure))
                if ancient:
                    messages.warning(
                        request, ("Desoler! Vous ne pouvez pas creer deux fois la meme election!"))
                    return redirect('/tontine/{}/'.format(idtontine))
                elec.creator = request.user
                tont = Tontine.objects.get(id=request.POST['idtontine'])
                elec.id_tontine = tont
                elec.save()
                messages.success(
                    request, ("Election Cree Avec Success Pour {}".format(tont.nom)))
                return redirect('/tontine/{}/'.format(elec.id_tontine.id))
            else:
                try:
                    messages.warning(
                        request, ('{}'.format(election.errors)))
                    return redirect('/creer_election/{}/'.format(idtontine))
                except:
                    messages.warning(
                        request, ("Erreur l\'ors de la creation de l\'election "))
                    return redirect('tontines')

        election = CreateElection

        tontine = Tontine.objects.get(id=idtontine)

        context['form'] = election
        context['nom'] = tontine.nom
        context['id'] = tontine.id

        return render(request, template, context)
    else:
        return redirect('login')

# DEPOSER UNE CANDIDATURE


def deposer_candidature(request, idtontine):

    template = 'tontine/create_candidature.html'
    context = {}

    tontine = Tontine.objects.get(id=idtontine)

    # election = Election.objects.filter(Q(id_tontine=tontine.id), date_gt=datetime.datetime.now)

    y, m, s = time.strftime("%Y-%m-%d").split('-')
    election = Election.objects.filter(id_tontine=tontine.id) & Election.objects.filter(
        date__gte=datetime.date(int(y), int(m), int(s))) & Election.objects.filter(date_fin_canditure__lte=datetime.date(int(y), int(m), int(s)))

    election = Election.objects.filter(
        Q(id_tontine=tontine.id) & Q(date_fin_canditure__gte=datetime.date(int(y), int(m), int(s))) & Q(date__gte=datetime.date(int(y), int(m), int(s)))).order_by('-date')
    # Election.objects.get(date=datetime.date(int(y), int(m), int(s)))
    mydict = []
    for elec in election:
        candidat = Candidat.objects.filter(id_election=elec.id)
        if Candidat.objects.filter(id_election=elec, id_user=request.user).exists():
            isCandidat = True
        else:
            isCandidat = False

        mydict.append(
            {'elections': elec, 'candidat': candidat, 'isCandidat': isCandidat})
    print(election)
    print(connection.queries)

    context['tontine'] = tontine

    context['election'] = election

    context['elect'] = mydict

    context['has_deposer'] = None

    return render(request, template, context)

# CONFIRMER LA CANDIDATURE


def confirmer_depos(request, idelection):

    template = 'tontine/depose_candidature.html'
    context = {}

    election = Election.objects.get(id=idelection)

    user = request.user

    cdt = Candidat.objects.filter(
        Q(id_election=election.id) & Q(id_user=user.id))

    if cdt:
        messages.warning(
            request, ("Impossible de deposer deux candidature a une meme election!"))
        return redirect('/tontine/{}/'.format(election.id_tontine.id))
    else:
        if request.method == 'POST':
            conf_depot = DeposerCandidature(request.POST or None)
            if conf_depot.is_valid():
                depot = conf_depot.save(commit=False)

                depot.id_election = election
                depot.id_user = user

                depot.save()
                messages.success(request, ("Candidature Deposer avec success"))
                return redirect('/tontine/{}/'.format(election.id_tontine.id))
            else:
                messages.warning(
                    request, ("Erreur L'ors de la confirmation de candidature"))
    form = DeposerCandidature

    context['form'] = form
    context['election'] = election

    return render(request, template, context)

# ENVOYER UNE NOTIFICATION


def envoyer_unenotification(request, idtontine):

    # tontine = request.GET.get('tontine')

    user = request.user

    tontine = Tontine.objects.get(id=idtontine)

    msg = str(user) + ' demande a integrer la tontine '+str(tontine.nom)

    Notification.objects.create(
        user=tontine.creator, sender=user, msg=msg, type_n='D', link='/accepter_demande/?idtontine={}&userid={}'.format(tontine.id, user.id))

    messages.success(request, ("Demande Envoyer avec success"))

    return redirect('home')

# RECEVOIR UNE NOTIFICATION


def recevoir_notification(request):

    template = 'tontine/notification.html'
    context = {}
    k = []
    notif = Notification.objects.filter(Q(user=request.user.id))
    for n in notif:
        k.append({'notification': n})
        # if MesTontine.objects.filter(id_membre=n.sender.id):
        #     k.append({'notification': n, 'present': True})
        # else:
        #     k.append({'notification': n, 'present': False})
    context['notifications'] = k

    return render(request, template, context)


def count_notif(request):
    # & Q(demande=False) & Q(type_n='D')).count()
    notif = Notification.objects.filter(
        Q(user=request.user.id) & Q(type_n='D') & Q(demande=False)).count()

    print(notif)

    return JsonResponse({"msg": notif})

# ACCEPTER_INVITATION


def accepter_invitation(request):

    idtontine = Tontine.objects.get(id=request.GET.get('idtontine'))
    userid = MyUser.objects.get(id=request.GET.get('userid'))

    notification = Notification.objects.get(
        id=request.GET.get('idnotification'))

    if MesTontine.objects.filter(id_tontine=idtontine, id_membre=userid).exists():
        notification.type_n = 'A'
        notification.save()
        return redirect('mes_notification')

    MesTontine.objects.create(id_tontine=idtontine,
                              id_membre=userid, nombre_de_part=1)
    notification.demande = True
    notification.type_n = 'A'
    notification.save()

    Notification.objects.create(type_n='A', sender=request.user, user=userid,
                                msg=f"{request.user} Vous a ajouter tontine {idtontine}", demande=True)

    return redirect('mes_notification')

# SELECTION UNE ELECTION


def selection_election(request, idtontine):
    template = 'tontine/liste_election.html'
    context = {}

    idtontine = Tontine.objects.get(id=idtontine)

    y, m, s = time.strftime("%Y-%m-%d").split('-')
    # election = Election.objects.filter(id_tontine=idtontine) & Election.objects.filter(
    #     date_fin_canditure__lte=datetime.date(int(y), int(m), int(s)))
    election = Election.objects.filter(
        Q(id_tontine=idtontine) & Q(date_fin_canditure__gte=datetime.date(int(y), int(m), int(s))) & Q(date__gte=datetime.date(int(y), int(m), int(s)))).order_by('-date')

    context['election'] = election

    return render(request, template, context)

# VOTER UN CANDIDAT A UNE ELECTIOn


def Voter(request, idelection):

    template = 'tontine/vote.html'
    context = {}

    election = Election.objects.get(id=idelection)

    candidat = Candidat.objects.filter(
        Q(id_election=election.id)).order_by('poste_canidat').query

    candidat.group_by = ['poste_canidat']

    candidat = QuerySet(query=candidat, model=Candidat)

    context['query'] = candidat

    context['election'] = election
    context['candidat'] = candidat

    return render(request, template, context)


def confirmer_vote(request):
    idelection = request.GET.get("idelection")
    idcandidat = request.GET.get("idcandidat")

    election = Election.objects.get(id=idelection)
    candidat = Candidat.objects.get(Q(id=idcandidat) & Q(id_election=election))

    _v = Vote.objects.filter(Q(candidat=candidat.id) & Q(
        election=election.id) & Q(member=request.user.id))

    _v = Vote.objects.filter(candidat=candidat.id,
                             election=election.id, member=request.user.id)
    already_vote = False

    if not _v.exists():
        for vote in Vote.objects.filter(Q(election=election)):
            if (vote.candidat.poste_canidat == candidat.poste_canidat) and (election.id == candidat.id_election.id) and (vote.member.id == request.user.id):
                already_vote = True
                print("Already Vote", already_vote)
                break
        if already_vote:
            messages.warning(request, ("Vous avec deja voter un candidate avec poste {}".format(
                candidat.poste_canidat)))
            return redirect('/voter/{}/'.format(election.id))
        else:
            Vote.objects.create(candidat=candidat,
                                election=election, member=request.user)
            candidat.nombre_de_voix += 1
            candidat.save()
            messages.success(request, ("Vote Effectuer avec success!"))
            return redirect('/voter/{}/'.format(election.id))
    else:

        messages.warning(request, ("Vous avec deja voter un candidate avec poste {}".format(
            candidat.poste_canidat)))
        return redirect('/voter/{}/'.format(election.id))


def confirmer_vote_president(request, idelection):
    template = 'tontine/choisir_candidat.html'
    context = {}

    election = Election.objects.get(id=idelection)
    PRES = 'President'
    candidat = Candidat.objects.filter(
        id_election=election, poste_canidat=PRES)

    already_vote = False

    vote = Vote.objects.filter(Q(election=election) & Q(
        member=request.user) & Q(candidat__in=candidat))

    if vote:
        already_vote = True
        print("Already Vote", already_vote)

    # if already_vote:
    #     messages.warning(
    #         request, ("Vous avec deja voter un candidate avec poste {}".format(PRES)))
    #     return redirect('/voter/{}/'.format(election.id))

    has_vote = False

    d = []

    for c in candidat:
        print(c.poste_canidat)
        test = (Vote.objects.filter(Q(candidat=c.id) & Q(
            election=election.id) & Q(member=request.user.id)))
        if test.exists() and c.poste_canidat == PRES:
            has_vote = already_vote
        else:
            has_vote = already_vote
        d.append({'candidat': c, 'hasvote': has_vote})

    context['election'] = election
    context['candidat'] = candidat
    context['cand_elec'] = d

    return render(request, template, context)


def confirmer_vote_tresorier(request, idelection):
    TRE = 'Tresorier'
    template = 'tontine/choisir_candidat.html'
    context = {}

    election = Election.objects.get(id=idelection)
    candidat = Candidat.objects.filter(
        id_election=election, poste_canidat=TRE)

    vote = Vote.objects.filter(Q(election=election) & Q(
        member=request.user) & Q(candidat__in=candidat))
    already_vote = False
    if vote:
        already_vote = True

    # if already_vote:
    #     messages.warning(
    #         request, ("Vous avec deja voter un candidate avec poste {}".format(TRE)))
    #     return redirect('/voter/{}/'.format(election.id))

    # print(connection.queries)

    has_vote = False

    d = []

    for c in candidat:
        print(c.poste_canidat)
        test = (Vote.objects.filter(Q(candidat=c.id) & Q(
            election=election.id))) & Vote.objects.filter(member=request.user.id)
        if test.exists() and c.poste_canidat == TRE:
            has_vote = True
        else:
            has_vote = False
        d.append({'candidat': c, 'hasvote': has_vote})

    context['election'] = election
    context['candidat'] = candidat
    context['cand_elec'] = d

    return render(request, template, context)


def confirmer_vote_secreataire(request, idelection):
    template = 'tontine/choisir_candidat.html'
    context = {}

    election = Election.objects.get(id=idelection)
    SC = 'Secretaire'
    candidat = Candidat.objects.filter(
        id_election=election, poste_canidat=SC)

    vote = Vote.objects.filter(Q(election=election) & Q(
        member=request.user) & Q(candidat__in=candidat))
    already_vote = False
    if vote:
        already_vote = True

    # if already_vote:
    #     messages.warning(
    #         request, ("Vous avec deja voter un candidate avec poste {}".format(SC)))
    #     return redirect('/voter/{}/'.format(election.id))

    # print(connection.queries)

    d = []

    for c in candidat:
        print(c.poste_canidat)
        test = (Vote.objects.filter(Q(candidat=c.id) & Q(
            election=election.id))) & Vote.objects.filter(member=request.user.id)
        if test.exists() and c.poste_canidat == SC:
            has_vote = already_vote
        else:
            has_vote = already_vote
        d.append({'candidat': c, 'hasvote': has_vote})

    context['election'] = election
    context['candidat'] = candidat
    context['cand_elec'] = d

    return render(request, template, context)


def confirmer_vote_commisaire(request, idelection):
    template = 'tontine/choisir_candidat.html'
    context = {}

    election = Election.objects.get(id=idelection)
    CAC = 'Commissaire aux Compte'
    candidat = Candidat.objects.filter(
        id_election=election, poste_canidat=CAC)

    vote = Vote.objects.filter(Q(election=election) & Q(
        member=request.user) & Q(candidat__in=candidat))
    already_vote = False
    if vote:
        already_vote = True

    if already_vote:
        messages.warning(
            request, ("Vous avec deja voter un candidate avec poste {}".format(CAC)))
        return redirect('/voter/{}/'.format(election.id))

    has_vote = False

    d = []

    for c in candidat:
        print(c.poste_canidat)
        test = (Vote.objects.filter(Q(candidat=c.id) & Q(
            election=election.id))) & Vote.objects.filter(member=request.user.id)
        if test.exists() and c.poste_canidat == CAC:
            has_vote = already_vote
        else:
            has_vote = already_vote
        d.append({'candidat': c, 'hasvote': has_vote})

    context['election'] = election
    context['candidat'] = candidat
    context['cand_elec'] = d

    return render(request, template, context)


def nombre_de_voix(candidat, election):

    candidat = candidat
    election = election
    liste_vote = Vote.objects.filter(
        election=election, candidat=candidat).count()

    return liste_vote


def resultat_election(request, idtontine):
    template = 'tontine/resultat_election.html'
    context = {}

    y, m, s = time.strftime("%Y-%m-%d").split('-')
    election = Election.objects.filter(id_tontine=idtontine).order_by('-date')
    cand = Candidat.objects.filter(
        id_election__in=election).order_by('poste_canidat')
    _d = []
    for elec in election:
        candidat = Candidat.objects.filter(id_election=elec.id)

        vo = Vote.objects.filter(Q(candidat__in=Candidat.objects.filter(
            id_election=elec)) & Q(election=elec))
        _d.append({'election': elec, 'candidat': candidat, 'votant': vo})

    context['el'] = _d

    # count number of voice

    vo = Vote.objects.filter(
        Q(candidat__in=Candidat.objects.filter(id_election__in=election)) & Q(election__in=election))
    context['vo'] = vo
    context['CCC'] = connection.queries

    return render(request, template, context)

# CREATION DUN FOND


def definire_membre_commiter(request, idelection):

    PRES = 'President'  # president
    TRE = 'Tresorier'  # tresorier
    SC = 'Secretaire'  # secraitaire
    CAC = 'Commissaire aux Compte'  # commissaire au compte

    election = Election.objects.get(id=idelection)

    candidat_president = Candidat.objects.filter(
        Q(id_election=election) & Q(poste_canidat=PRES))

    candidat_tresorier = Candidat.objects.filter(
        Q(id_election=election) & Q(poste_canidat=TRE))

    candidat_secretaire = Candidat.objects.filter(
        Q(id_election=election) & Q(poste_canidat=SC))

    candidat_commisaire = Candidat.objects.filter(
        Q(id_election=election) & Q(poste_canidat=CAC))


def creer_fond(request, idtontine):

    template = 'tontine/creer_fond.html'
    context = {}

    tont = Tontine.objects.get(id=idtontine)

    if request.method == 'POST':
        fond = CreateFond(request.POST)

        if fond.is_valid():
            fond_tontine = fond.save(commit=False)
            fond_tontine.id_tontine = tont
            fond.save()
            messages.success(
                request, ("Fond {} Creer avec success pour {}".format(fond.nom, tont)))
            return redirect('/tontine/{}/'.format(idtontine))
        else:
            messages.warning(
                request, ("Erreur souvenue l'ors de la creation du fond veillier recommencer!"))
            return redirect('/tontine/{}/'.format(idtontine))

    fond = CreateFond

    context['form'] = fond

    return render(request, template, context)


def modifier_profile(request):
    if request.user.is_authenticated:
        template = 'tontine/modify.html'
        context = {}

        form = UserCreationForm(instance=request.user)

        if request.method == 'POST':
            form = UserCreationForm(
                request.POST, request.FILES, instance=request.user)

            if form.is_valid():
                form.save()
                username = request.POST['email']
                password = request.POST['password1']
                _user = authenticate(
                    request, username=username, password=password)

                if _user is not None:
                    login(request, _user)
                return redirect('/profile/{}/'.format(request.user.id))

        context['form'] = form

        return render(request, template, context)
    else:
        return redirect('login')


def creer_cotisation(request, idtontine):
    template = 'tontine/create_cotisation.html'
    context = {}

    tontine = Tontine.objects.get(id=idtontine)

    if request.method == 'POST':
        cotisation = CreateCotisation(request.POST)

        if cotisation.is_valid():
            cot = cotisation.save(commit=False)
            cot.id_tontine = tontine
            cot.creator = request.user

            cot.save()
            messages.success(
                request, ("Cotisation {} creer avec success ".format(cot.nom_cotisation)))
            return redirect('/tontine/{}/'.format(idtontine))

        else:
            messages.warning(
                request, ("Erreur Souvenue l'or de la creation de cotisation"))
            return redirect('/tontine/{}/'.format(idtontine))

    form = CreateCotisation

    context['form'] = form

    return render(request, template, context)
