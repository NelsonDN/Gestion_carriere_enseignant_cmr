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
        
        try:
            proviseur = Poste.objects.get(pk = 1)
        except:
            print('proooooooooooo')

        surveillantG = poste
        try:
            surveillantG = Poste.objects.get(pk = 2)
        except:
            print('sssssssssssssssssss')

        try:
            censeur = Poste.objects.get(pk = 3)
        except:
            print('cccccccccccccccccccccccccccc')

        all_proviseur =  Etablissement_Poste.objects.filter(poste = proviseur).filter(user__isnull=False).values_list('user', flat=True)
        all_censeur =  Etablissement_Poste.objects.filter(poste = censeur).filter(user__isnull=False).values_list('user', flat=True)
            
        # les departement de postes 
        departements = Departement.objects.all()
        employe_ids = Etablissement_Poste.objects.all().filter(user__isnull=False).values_list('user', flat=True)
        # print("emploooooooooooo")
        # print(employe_ids)
        all_employe_ids =  Etablissement_Poste.objects.filter(etablissement = etablissement).filter(poste = poste).filter(user__isnull=False).values_list('user', flat=True)
        print("oirginnnnnnnnn")
        print(all_employe_ids) 
        departement_ids = ProfilEnseignant.objects.filter(user__in = all_employe_ids).values_list('departementOrigine', flat=True)
        # profils = ProfilEnseignant.objects.exclude(departementOrigine__in = employe_ids).exclude(user__in = all_employe_ids)

        # dernier_carriere = Carriere.objects.filter(user = instance.user).order_by('-id').first()
        # dernier_carriere.anneeDepart = date.today()
        # dernier_carriere.poste = etablissementPoste
        # dernier_carriere.save()


        # Filtrer les profils dont l'ancienneté est de anciennete_min ans ou plus
        anciennete_min = poste.anciennete_min
        # Calculer l'année actuelle
        anneeCourante = now().year
        # print("ANNEEEEEEEEEEEEEEEEEEEEE")
        # print(anneeCourante)

        # censeur les matieres 
        if poste.is_censeur:
            profil_enseignant_eligible_ids = ProfilEnseignant.objects.annotate(
                anciennete=anneeCourante - F('anneeSortie__year')
            ).filter(anciennete__gte=anciennete_min
            ).filter(matiere = poste.matiere
            ).exclude(user__in = all_proviseur
            ).exclude(user__in = all_censeur
            ).exclude(departementOrigine__in = departement_ids
            ).values_list('user', flat=True)
        elif poste.id == surveillantG.id:
            profil_enseignant_eligible_ids = ProfilEnseignant.objects.annotate(
                anciennete=anneeCourante - F('anneeSortie__year')
            ).filter(anciennete__gte=anciennete_min
            ).exclude(user__in = all_censeur
            ).exclude(user__in = all_proviseur
            ).exclude(departementOrigine__in = departement_ids
            ).values_list('user', flat=True)
        else:
            profil_enseignant_eligible_ids = ProfilEnseignant.objects.annotate(
                anciennete=anneeCourante - F('anneeSortie__year')
            ).filter(anciennete__gte=anciennete_min
            ).exclude(user__in = all_proviseur
            ).exclude(departementOrigine__in = departement_ids
            ).values_list('user', flat=True)
            # profil_enseignant_eligible_ids = ProfilEnseignant.objects.annotate(
            #     anciennete=anneeCourante - F('anneeSortie__year')
            # ).exclude(departementOrigine__in = employe_ids
            # ).exclude(user__in = all_employe_ids
            # ).filter(anciennete__gte=anciennete_min
            # ).filter(etablissement=etablissement
            # ).values_list('user', flat=True)
            # print("anciennnnnete")
            # for profil in profil_enseignant_eligible_ids:
            #     print(profil.anciennete)
            # print("PORFILLLLLLLLLL")
            # print(profil_enseignant_eligible_ids)

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
    # dateNaissance = forms.DateField(label="Date de Naissance",
    #         widget=forms.DateInput(
    #             attrs={
    #                 'class': 'form-control',
    #                 'type': 'date'
    #             }
    #         ))  
    # anneeSortie = forms.DateField(label="Année de sortie", 
    #         widget=forms.DateInput(
    #             attrs={
    #                 'class': 'form-control',
    #                 'type': 'date'
    #             }
    #         ))  
    matricule = forms.CharField(label="Matricule")  
    telephone = forms.CharField(label="Téléphone")  
    sexes = [('M', 'Masculin'), ('F', "Féminin")]
    sexe = forms.ChoiceField(label = "Catégorie", choices = sexes)

    situations = [('Marié(e)', 'Marié(e)'), ('Célibataire', "Célibataire")]
    situationMatrimoniale = forms.ChoiceField(label = "Situation Matrimoniale", choices = situations)
    categories = [('A1', 'A1'), ('A2', "A2")]
    categorie = forms.ChoiceField(label = "Catégorie", choices = categories)
    
    class Meta:
        model = ProfilEnseignant
        fields = ['departementOrigine', 'etablissement', 'cv', 'dateNaissance', 'anneeSortie', 'matricule', 'categorie', 'situationMatrimoniale']
