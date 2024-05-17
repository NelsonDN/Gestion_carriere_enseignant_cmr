# Generated by Django 5.0.3 on 2024-05-16 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionministere', '0003_profilenseignant_sexe_profilenseignant_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carriere',
            name='discipline',
            field=models.TextField(blank=True, max_length=64, null=True, verbose_name='Discipline'),
        ),
        migrations.AlterField(
            model_name='carriere',
            name='etablissement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionministere.etablissement'),
        ),
        migrations.AlterField(
            model_name='carriere',
            name='performance',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Performance'),
        ),
        migrations.AlterField(
            model_name='carriere',
            name='poste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionministere.poste'),
        ),
    ]
