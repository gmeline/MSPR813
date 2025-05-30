from django.db import models

class CriminalityPerCir(models.Model):
    # Django adds an 'id' AutoField primary key automatically
    code_circonscription = models.TextField(
        null=True, blank=True, db_column='code_circonscription',
        help_text="Code identifying the circonscription"
    )
    annee = models.IntegerField(
        null=True, blank=True, db_column='annee',
        help_text="Year of the data"
    )
    nombre = models.IntegerField(
        null=True, blank=True, db_column='nombre',
        help_text="Number of criminal incidents"
    )
    population = models.IntegerField(
        null=True, blank=True, db_column='population',
        help_text="Population of the circonscription for that year"
    )
    taux_pour_mille = models.FloatField(
        null=True, blank=True, db_column='taux_pour_mille',
        help_text="Criminality rate per thousand inhabitants"
    )

    class Meta:
        db_table = 'criminality_per_cir'

class LegislativePerCir(models.Model):
    code_du_departement = models.IntegerField(null=True, blank=True)
    libelle_du_departement = models.TextField(null=True, blank=True)
    code_de_la_circonscription = models.TextField(null=True, blank=True)
    inscrits = models.IntegerField(null=True, blank=True)
    votants = models.IntegerField(null=True, blank=True)
    exprimes = models.IntegerField(null=True, blank=True)
    blancs_et_nuls = models.IntegerField(null=True, blank=True)
    nuance = models.TextField(null=True, blank=True)
    voix = models.IntegerField(null=True, blank=True)
    nuance_2 = models.TextField(null=True, blank=True)
    voix_2 = models.IntegerField(null=True, blank=True)
    nuance_3 = models.TextField(null=True, blank=True)
    voix_3 = models.IntegerField(null=True, blank=True)
    annee = models.IntegerField(null=True, blank=True)
    gagnant = models.TextField(null=True, blank=True)
    voix_gagnant = models.IntegerField(null=True, blank=True)
    gagnant_precedent = models.TextField(null=True, blank=True)
    voix_gagnant_precedent = models.IntegerField(null=True, blank=True)

    encodage_sans_centre_nuance = models.IntegerField(null=True, blank=True)
    encodage_avec_centre_nuance = models.IntegerField(null=True, blank=True)
    encodage_centre_extremes_nuance = models.IntegerField(null=True, blank=True)

    encodage_sans_centre_nuance_2 = models.IntegerField(null=True, blank=True)
    encodage_avec_centre_nuance_2 = models.IntegerField(null=True, blank=True)
    encodage_centre_extremes_nuance_2 = models.IntegerField(null=True, blank=True)

    encodage_sans_centre_nuance_3 = models.IntegerField(null=True, blank=True)
    encodage_avec_centre_nuance_3 = models.IntegerField(null=True, blank=True)
    encodage_centre_extremes_nuance_3 = models.IntegerField(null=True, blank=True)

    encodage_sans_centre_gagnant = models.IntegerField(null=True, blank=True)
    encodage_avec_centre_gagnant = models.IntegerField(null=True, blank=True)
    encodage_centre_extremes_gagnant = models.IntegerField(null=True, blank=True)

    encodage_sans_centre_gagnant_precedent = models.IntegerField(null=True, blank=True)
    encodage_avec_centre_gagnant_precedent = models.IntegerField(null=True, blank=True)
    encodage_centre_extremes_gagnant_precedent = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'legislative_per_cir'

class UnemploymentPerCir(models.Model):
    id = models.AutoField(primary_key=True)
    code_circonscription = models.TextField(blank=True, null=True)
    annee = models.IntegerField(blank=True, null=True)
    populationauth_groupunemployment_per_cir = models.IntegerField(blank=True, null=True)
    chomeurs = models.IntegerField(blank=True, null=True)
    taux_chomage = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'unemployment_per_cir'

class DensityPopulation(models.Model):
    id = models.AutoField(primary_key=True)
    code_departement = models.IntegerField(blank=True, null=True)
    density = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'density_population'