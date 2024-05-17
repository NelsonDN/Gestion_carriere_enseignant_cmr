from django.db import models
from gestionministere.models import Region, Departement, Etablissement, Poste, Etablissement_Poste, Enseignant, Matiere, ProfilEnseignant, Carriere


# class Nomination(Etablissement_Poste):
    
#     class Meta:
#         proxy = True

#     def __str__(self):
#         valeur = self.etablissement.name  or ""
#         return f"{valeur} - {self.poste.name}".strip()
    
#     class Meta:
#         verbose_name = "Nomination"
#         verbose_name_plural = "Gestion des Nominations"