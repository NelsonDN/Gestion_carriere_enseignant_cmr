# Generated by Django 5.0.3 on 2024-06-04 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionministere', '0008_profilenseignant_dernieranneeverif_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilenseignant',
            name='poste',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestionministere.poste'),
        ),
    ]