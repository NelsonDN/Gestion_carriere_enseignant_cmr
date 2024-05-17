from django.apps import AppConfig


class GestionministereConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestionministere'

    verbose_name = "Gestion des données"
    def ready(self):
        import gestionministere.models 