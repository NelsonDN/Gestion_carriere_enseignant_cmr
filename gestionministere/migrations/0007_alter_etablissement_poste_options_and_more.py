# Generated by Django 5.0.3 on 2024-05-17 00:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionministere', '0006_poste_is_censeur_poste_matiere'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='etablissement_poste',
            options={'verbose_name': 'Nomination', 'verbose_name_plural': 'Gestion des Nominations'},
        ),
        migrations.AlterField(
            model_name='poste',
            name='is_censeur',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Est censeur ?'),
        ),
        migrations.AlterField(
            model_name='poste',
            name='matiere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionministere.matiere', verbose_name='De quelle matiere ?'),
        ),
    ]
