# Generated by Django 5.0.3 on 2024-05-16 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionministere', '0005_profilenseignant_avancement'),
    ]

    operations = [
        migrations.AddField(
            model_name='poste',
            name='is_censeur',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='poste',
            name='matiere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionministere.matiere'),
        ),
    ]