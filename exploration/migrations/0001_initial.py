# Generated by Django 5.1.6 on 2025-04-14 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ResultatElection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code_du_departement", models.CharField(max_length=10)),
                ("libelle_du_departement", models.CharField(max_length=50)),
                ("code_de_la_circonscription", models.CharField(max_length=10)),
                ("inscrits", models.IntegerField()),
                ("votants", models.IntegerField()),
                ("exprimes", models.IntegerField()),
                ("blancs_et_nuls", models.IntegerField()),
                ("nuance", models.CharField(max_length=10)),
                ("voix", models.IntegerField()),
                ("nuance_2", models.CharField(blank=True, max_length=10, null=True)),
                ("voix_2", models.IntegerField(blank=True, null=True)),
                ("nuance_3", models.CharField(blank=True, max_length=10, null=True)),
                ("voix_3", models.IntegerField(blank=True, null=True)),
                ("annee", models.IntegerField()),
            ],
        ),
    ]
