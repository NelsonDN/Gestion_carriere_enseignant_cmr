from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from gestionministere.models import Region, Departement, Etablissement, Poste, Etablissement_Poste, Enseignant, Matiere, ProfilEnseignant, Carriere
from gestionministere.forms import EnseignantCreationForm, ProfileEnseignantForm, EnseignantEditForm
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg
from datetime import date
from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe
# Register your models here.


