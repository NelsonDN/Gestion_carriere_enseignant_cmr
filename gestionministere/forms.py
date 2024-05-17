from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Region, Departement, Etablissement, Poste, Etablissement_Poste, Enseignant, Matiere, ProfilEnseignant, Carriere
from django.contrib.auth.models import User
from django.db.models import F
from django.utils.timezone import now

class Etablissement_PosteForm(forms.ModelForm):

    class Meta:
        model = Etablissement_Poste
        fields = ['etablissement', 'poste', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Récupérer les matières où user est null ou égal à l'utilisateur en question
        etablissementposte = kwargs['instance']
        etablissement = Etablissement.objects.get(pk = etablissementposte.etablissement.id)
        poste = Poste.objects.get(pk = etablissementposte.poste.id)

        # les departement de postes 
        departements = Departement.objects.all()
        employe_ids = Etablissement_Poste.objects.filter(etablissement=etablissement, poste=poste).values_list('user', flat=True)
        all_employe_ids =  Etablissement_Poste.objects.all().values_list('user', flat=True)
        departement_ids = ProfilEnseignant.objects.filter(user__in = employe_ids).values_list('departementOrigine', flat=True)
        # profils = ProfilEnseignant.objects.exclude(departementOrigine__in = employe_ids).exclude(user__in = all_employe_ids)

        # Filtrer les profils dont l'ancienneté est de anciennete_min ans ou plus
        anciennete_min = poste.anciennete_min
        # Calculer l'année actuelle
        anneeCourante = now().year

        # censeur les matieres 
        if poste.is_censeur:
            profil_enseignant_eligible_ids = ProfilEnseignant.objects.annotate(
                anciennete=anneeCourante - F('anneeSortie__year')
            ).exclude(departementOrigine__in = employe_ids
            ).exclude(user__in = all_employe_ids
            ).filter(anciennete__gte=anciennete_min
            ).filter(matiere = poste.matiere
            ).values_list('user', flat=True)
        else:
            profil_enseignant_eligible_ids = ProfilEnseignant.objects.annotate(
                anciennete=anneeCourante - F('anneeSortie__year')
            ).exclude(departementOrigine__in = employe_ids
            ).exclude(user__in = all_employe_ids
            ).filter(anciennete__gte=anciennete_min
            ).values_list('user', flat=True)

        users = User.objects.filter(pk__in = profil_enseignant_eligible_ids)

        # queryset = Poste.objects.filter(user__isnull=True) | Poste.objects.filter(user=user)
        self.fields['user'].queryset = users

class EnseignantCreationForm(UserCreationForm):
    username = forms.CharField(label="Nom de l'enseignant")  
    
    class Meta:
        model = Enseignant
        fields = ['username', 'email', 'password1', 'password2']

class EnseignantEditForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['username', 'email']


class ProfileEnseignantForm(forms.ModelForm):
    departementOrigine = forms.ModelChoiceField(queryset= Departement.objects.all(), label="Département d'origine")
    etablissement = forms.ModelChoiceField(queryset= Etablissement.objects.all(), label="Etablissement")
    matiere = forms.ModelChoiceField(queryset= Matiere.objects.all(), label="Spécialité")

    cv = forms.FileField(label="CV")  
    dateNaissance = forms.DateField(label="Date de Naissance",
            widget=forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ))  
    anneeSortie = forms.DateField(label="Année de sortie", 
            widget=forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ))  
    matricule = forms.CharField(label="Matricule")  
    telephone = forms.CharField(label="Téléphone")  
    sexes = [('M', 'Masculin'), ('F', "Féminin")]
    sexe = forms.ChoiceField(label = "Catégorie", choices = sexes)

    situations = [('Marié(e)', 'Marié(e)'), ('Célibataire', "Célibataire")]
    situationMatrimoniale = forms.ChoiceField(label = "Situation Matrimoniale", choices = situations)
    categories = [('A1', 'A1'), ('A2', "A2")]
    categorie = forms.ChoiceField(label = "Catégorie", choices = categories)
    
    class Meta:
        model = Enseignant
        fields = ['departementOrigine', 'etablissement', 'cv', 'dateNaissance', 'anneeSortie', 'matricule', 'categorie', 'situationMatrimoniale']
