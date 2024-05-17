from django.urls import path
from . import views


app_name = "gestionministere"

urlpatterns = [
    path('', views.home, name = 'home'),
    path('enseignants/details/<int:user_id>/', views.show_enseignant, name = 'show_enseignant'),
    path('download/cv/<int:user_id>/', views.download_cv, name = 'download_cv'),
]

