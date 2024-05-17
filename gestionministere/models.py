from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import date


class Region(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")

    def __str__(self):
        valeur = self.name  or ""
        return  f"{valeur}".strip()
    
    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"

class Departement(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        valeur = self.name  or ""
        return  f"{valeur}".strip()
    
    class Meta:
        verbose_name = "Departement"
        verbose_name_plural = "Departements"

class Matiere(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name= "Nom")

    def __str__(self):
        valeur = self.name  or ""
        return  f"{valeur}".strip()
    
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"

class Poste(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name= "Nom")
    anciennete_min = models.IntegerField(default=1, null=True, blank=True, verbose_name= "Ancienneté min")
    is_censeur = models.BooleanField(default=False, null=True, blank=True, verbose_name= "Est censeur ?")
    matiere = models.ForeignKey(Matiere, null=True, blank=True, on_delete=models.CASCADE, verbose_name= "De quelle matiere ?")

    def __str__(self):
        valeur = self.name  or ""
        return  f"{valeur}".strip()
    
    class Meta:
        verbose_name = "Poste administratif"
        verbose_name_plural = "Postes"


class Etablissement(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name= "Nom")
    BP = models.CharField(max_length=64, null=True, blank=True, verbose_name= "BP")
    email = models.CharField(max_length=64, unique=True, verbose_name= "email")
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, verbose_name= "Departement")
    poste = models.ManyToManyField(Poste, through='Etablissement_Poste')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Etablissement"
        verbose_name_plural = "Etablissements"

class Etablissement_Poste(models.Model):
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE)
    poste = models.ForeignKey(Poste, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Enseignant éligible")

    def __str__(self):
        valeur = self.etablissement.name  or ""
        return f"{valeur} - {self.poste.name}".strip()
    
    class Meta:
        verbose_name = "Nomination"
        verbose_name_plural = "Gestion des Nominations"

class Enseignant(User):
    
    class Meta:
        proxy = True

    def __str__(self):
        valeur = self.username  or ""
        return  f"{valeur}".strip()

class ProfilEnseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, null=True, blank=True, on_delete=models.CASCADE)
    departementOrigine = models.ForeignKey(Departement, on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE)
    cv = models.FileField(upload_to ='enseignant_cvs/', verbose_name= "CV")
    dateNaissance = models.DateField(null=True, blank=True, verbose_name= "Date de naissance")
    anneeSortie = models.DateField(verbose_name= "Année de sortie")
    matricule = models.CharField(max_length=64, unique=True, verbose_name= "Matricule")
    telephone = models.CharField(max_length=64, null=True, blank=True, verbose_name= "Numéro de télephone")
    sexe = models.CharField(max_length=64, null=True, blank=True, verbose_name= "Sexe")
    situationMatrimoniale = models.CharField(max_length=64, verbose_name= "Situation Matrimoniale")
    categorie = models.CharField(max_length=64, verbose_name= "Categorie")
    avancement = models.IntegerField(default=0, null=True, blank=True, verbose_name= "Avancement")


    def __str__(self):
        valeur = self.matricule  or ""
        return  f"{valeur}".strip()
    
    def formatted_telephone(self):
        number = self.telephone
        if len(number) < 2:
            return number
        return f"{number[0]} " + ' '.join(number[i:i+2] for i in range(1, len(number), 2))
    
    class Meta:
        verbose_name = "Profil Enseignant"
        verbose_name_plural = "Profils Enseignant"

class Carriere(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poste = models.ForeignKey(Poste, null=True, blank=True, on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Etablissement, null=True, blank=True, on_delete=models.CASCADE)
    anneeArrive = models.DateField(null=True, blank=True, verbose_name= "Année d'entrée")
    anneeDepart = models.DateField(null=True, blank=True, verbose_name= "Année de sortie")
    performance = models.CharField(max_length=64, null=True, blank=True, verbose_name= "Performance")
    discipline = models.TextField(max_length=64, null=True, blank=True, verbose_name= "Discipline")

    def __str__(self):
        valeur = self.user.username  or ""
        return  f"{valeur}".strip()
    
    class Meta:
        verbose_name = "Carriere"
        verbose_name_plural = "Carrieres"

@receiver(post_save, sender=ProfilEnseignant)
def handle_profile_creation_or_update(sender, instance, created, **kwargs):
    if created:
        # Créer un enregistrement Carriere après la création d'un ProfilEnseignant
        Carriere.objects.create(
            user=instance.user,
            etablissement=instance.etablissement,
            anneeArrive=instance.anneeSortie,
        )
        print("Un ProfilEnseignant a été créé avec l'utilisateur :", instance.user)
    else:
        # Traiter la mise à jour du ProfilEnseignant ici
        # Vous pouvez effectuer des vérifications spécifiques et des mises à jour
        print("Un ProfilEnseignant a été modifié pour l'utilisateur :", instance.user)

@receiver(pre_save, sender=ProfilEnseignant)
def handle_profile_pre_update(sender, instance, **kwargs):
    if instance.pk:
        previous = ProfilEnseignant.objects.get(pk=instance.pk)
        # Comparez les champs anciens et nouveaux pour voir s'il y a des modifications
        if previous.etablissement != instance.etablissement:
            # Récupérer le dernier enregistrement de Carriere pour cet utilisateur
            dernier_carriere = Carriere.objects.filter(user = instance.user).order_by('-id').first()
            dernier_carriere.anneeDepart = date.today()
            dernier_carriere.save()

            Carriere.objects.create(
                user=instance.user,
                etablissement=instance.etablissement,
                anneeArrive=date.today(),
            )
            # Faire quelque chose si des champs spécifiques ont été modifiés
            print("Un ProfilEnseignant est sur le point d'être modifié pour l'utilisateur :", instance.user)