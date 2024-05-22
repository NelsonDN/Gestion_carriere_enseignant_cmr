from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Region, Departement, Etablissement, Poste, Etablissement_Poste, Enseignant, Matiere, ProfilEnseignant, Carriere
from .forms import EnseignantCreationForm, ProfileEnseignantForm, EnseignantEditForm, Etablissement_PosteForm
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg
from datetime import date
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe
from .views import avancement
# Register your models here.
class PosteInline(admin.TabularInline):
    model = Etablissement.poste.through
    fields = ('poste',)

class ProfileInline(admin.StackedInline):
    form = ProfileEnseignantForm
    model = ProfilEnseignant

@admin.register(Etablissement_Poste)
class Etablissement_PosteAdmin(admin.ModelAdmin):
    fields = ['etablissement', 'poste', 'user']

    list_display = ('etablissement', 'poste', 'user')
    list_filter = ['etablissement']
    list_per_page = 10

    def get_form(self, request, obj=None, **kwargs):
        if obj:  # Vérifie si un objet est en cours d'édition
            return Etablissement_PosteForm
        return super().get_form(request, obj, **kwargs)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10
    

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    fields = ['name', 'region']
    list_display = ('name', 'region')
    list_filter = ['name', 'region__name']
    search_fields = ['name']
    list_per_page = 10

@admin.register(Poste)
class PosteAdmin(admin.ModelAdmin):

    class Media:
        js = ('admin/js/admin.js',)

    fields = ['name', 'anciennete_min', 'is_censeur', 'matiere']
    list_display = ('name', 'anciennete_min', 'is_censeur', 'matiere')
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10

@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    fields = ['name', 'BP', 'email', 'departement']

    list_display = ('name', 'BP', 'email', 'departement', 'Gerer_les_postes', 'Gerer_les_enseignants')
    list_filter = ['name', 'departement']
    search_fields = ['departement__name', 'name']
    list_per_page = 10
    def Gerer_les_postes(self, obj):
        return format_html('<a href="/admin/gestionministere/etablissement_poste/?etablissement__id__exact={}">Gérer les postes</a>'.format(obj.id))
    Gerer_les_postes.allow_tags = True
    Gerer_les_postes.short_description = "Gérer les postes"

    def Gerer_les_enseignants(self, obj):
        return format_html('<a href="/admin/gestionministere/profilenseignant/?etablissement__id__exact={}">Consulter</a>'.format(obj.id))
    Gerer_les_enseignants.allow_tags = True
    Gerer_les_enseignants.short_description = "Liste Enseignant"

    inlines = [PosteInline]

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']
    list_per_page = 10

class EnseignantAdmin(admin.ModelAdmin):
    form = EnseignantCreationForm

    list_display = ('nom_enseignant', 'email', 'etablissement', 'anneeSortie', 'matricule', 'specialite', 'avancement', 'Consulter_carriere')
    inlines = [ProfileInline]

    def get_form(self, request, obj=None, **kwargs):
        if obj:  # Vérifie si un objet est en cours d'édition
            return EnseignantEditForm
        return super().get_form(request, obj, **kwargs)
    
    def Consulter_carriere(self, obj):
        return format_html('<a href="/admin/gestionministere/carriere/?user__id__exact={}">Consulter</a>'.format(obj.id))
    Consulter_carriere.allow_tags = True
    Consulter_carriere.short_description = "Historique carrière"
    
    def custom_action(modeladmin, request, queryset):
        for obj in queryset:
            avancement(obj)
        
        modeladmin.message_user(request, "La mise à jour des avancements a été exécutée avec succès!")
    custom_action.short_description = "LANCER LA MISE A JOUR DES AVANCEMENTS"

    actions=[custom_action]

    def nom_enseignant(self, obj):
        return obj.username
    
    def etablissement(self, obj):
        profil = ProfilEnseignant.objects.get(user=obj)
        return profil.etablissement.name 
    
    def anneeSortie(self, obj):
        profil = ProfilEnseignant.objects.get(user=obj)
        return profil.anneeSortie 
    
    def departement(self, obj):
        profil = ProfilEnseignant.objects.get(user=obj)
        return profil.departementOrigine.name
    
    def matricule(self, obj):
        profil = ProfilEnseignant.objects.get(user=obj)
        return profil.matricule
    
    def specialite(self, obj):
        profil = ProfilEnseignant.objects.get(user=obj)
        return profil.matiere.name
        
    def avancement(self, obj):
        profil = ProfilEnseignant.objects.get(user=obj)
        return profil.avancement
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)

admin.site.register(Enseignant, EnseignantAdmin)

@admin.register(Carriere)
class CarriereAdmin(admin.ModelAdmin):
    fields = ['user','etablissement','performance', 'discipline', 'anneeArrive', 'anneeDepart']

    list_display = ('user', 'poste', 'anneeArrive', 'anneeDepart', 'etablissement')
    list_filter = ['user']
    list_per_page = 10

@admin.register(ProfilEnseignant)
class ProfilAdmin(admin.ModelAdmin):
    fields = ['user', 'matricule', 'etablissement']

    list_display = ('user', 'matricule', 'etablissement', 'anneeSortie')
    list_filter = ['user']
    list_per_page = 10