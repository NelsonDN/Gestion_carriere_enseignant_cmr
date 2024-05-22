from .models import Region, Departement, Etablissement, Poste, Etablissement_Poste, Enseignant, Matiere, ProfilEnseignant, Carriere
from django.http import HttpResponse, HttpResponseBadRequest, FileResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from mimetypes import guess_type
from django.db.models import Q
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta


def is_not_superuser(user):
    return user.is_superuser == False

def is_user_authenticated(user, user_id):
    return user.is_authenticated and user.id == user_id

def home(request):
    user = request.user

    users = User.objects.filter(is_superuser=False)
    regions = Region.objects.all()
    departements = Departement.objects.all()

    if request.method == 'POST':
        region_id = request.POST.get('region_id')
        departement_id = request.POST.get('departement_id')
        user_name = request.POST.get('user_name')

        query = Q()

        if region_id:
            query |= Q(departementOrigine__etablissement__departement__region_id=region_id)

        if departement_id:
            query |= Q(departementOrigine__etablissement__departement_id=departement_id)

        if user_name:
            query |= Q(user__username__icontains=user_name) | Q(user__first_name__icontains=user_name) | Q(user__last_name__icontains=user_name)

        profils_enseignant = ProfilEnseignant.objects.filter(query).select_related('user')
        users = []

        for profil_enseignant in profils_enseignant:
            users.append(profil_enseignant.user)
        print(users)

    context = {
        "user": user,
        "regions": regions,
        "departements": departements,
        "users": users,
    }
    return render(request,"gestionministere/index.html", context)

@user_passes_test(is_not_superuser)
@login_required
def show_enseignant(request, user_id):
    if not is_user_authenticated(request.user, user_id):
        return HttpResponseForbidden("Accès refusé")
    
    user = User.objects.get(pk = user_id)
    profil = ProfilEnseignant.objects.get(user = user)
    poste_user = None
    try:
        poste_user = Etablissement_Poste.objects.get(user=user)
    except:
        poste_user = None

    carrieres = Carriere.objects.filter(user=user)

    context = {
        "user": user,
        "profil": profil,
        "poste_user":poste_user,
        "carrieres": carrieres
    }
    
    return render(request,"gestionministere/details.html", context)

# def increment_avancement_view(request):
#     enseignants = ProfilEnseignant.objects.all()
#     current_year = now().year
    
#     for enseignant in enseignants:
#         years_since_graduation = current_year - enseignant.anneeSortie.year
#         expected_avancement = years_since_graduation // 2
        
#         if enseignant.avancement < expected_avancement:
#             enseignant.avancement = expected_avancement
#             enseignant.save()

#     return HttpResponse("Terminé avec succès")

def increment_avancement_view(request):
    enseignants = ProfilEnseignant.objects.all()
    current_date = now().date()
    
    for enseignant in enseignants:
        annee_sortie = enseignant.anneeSortie
        # Utiliser relativedelta pour calculer la différence en années
        difference = relativedelta(current_date, annee_sortie)
        years_since_graduation = difference.years
        
        # Calculer le nombre attendu d'avancements
        expected_avancement = years_since_graduation // 2
        
        if enseignant.avancement < expected_avancement:
            enseignant.avancement = expected_avancement
            enseignant.save()

    return HttpResponse("Avancement updated successfully for all enseignants.")

@user_passes_test(is_not_superuser)
@login_required
def download_cv(request, user_id):
    profil = get_object_or_404(ProfilEnseignant, user_id=user_id)
    cv = profil.cv
    
    if not cv:
        raise Http404("CV non trouvé")

    # Deviner le type MIME du fichier
    mime_type, _ = guess_type(cv.path)
    # Si le type MIME ne peut pas être deviné, utiliser un type générique
    if not mime_type:
        mime_type = 'application/octet-stream'

    # Ouvrir le fichier CV en mode binaire
    with open(cv.path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=mime_type)
        # Ajouter les en-têtes pour forcer le téléchargement du fichier
        response['Content-Disposition'] = f'attachment; filename={cv.name}'
        return response