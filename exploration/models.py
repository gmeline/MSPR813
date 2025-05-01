from django.db import models

class ResultatElection(models.Model):
    code_du_departement = models.CharField(max_length=10)
    libelle_du_departement = models.CharField(max_length=50)
    code_de_la_circonscription = models.CharField(max_length=10)
    inscrits = models.IntegerField()
    votants = models.IntegerField()
    exprimes = models.IntegerField()
    blancs_et_nuls = models.IntegerField()
    nuance = models.CharField(max_length=10)
    voix = models.IntegerField()
    nuance_2 = models.CharField(max_length=10, blank=True, null=True)
    voix_2 = models.IntegerField(blank=True, null=True)
    nuance_3 = models.CharField(max_length=10, blank=True, null=True)
    voix_3 = models.IntegerField(blank=True, null=True)
    annee = models.IntegerField()
    gagnant = models.CharField(max_length=30)
    voix_gagnant = models.CharField(max_length=30)
    gagnant_precedent = models.CharField(max_length=10)
    voix_gagnant_precedent = models.IntegerField()
    encodage_sans_centre_gagnant = models.IntegerField()
    encodage_avec_centre_gagnant = models.IntegerField()
    encodage_centre_extremes_gagnant = models.IntegerField()
    encodage_sans_centre_gagnant_precedent = models.IntegerField()
    encodage_avec_centre_gagnant_precedent = models.IntegerField()
    encodage_centre_extremes_gagnant_precedent = models.IntegerField()
    instabilite_sans_centre = models.IntegerField()
    poids_nuance_sans_centre = models.IntegerField()
    desir_changement_sans_centre = models.IntegerField()
    instabilite_avec_centre = models.IntegerField()
    poids_nuance_avec_centre = models.IntegerField()
    desir_changement_avec_centre = models.IntegerField()
    instabilite_centre_extremes = models.IntegerField()
    poids_nuance_centre_extremes = models.IntegerField()
    desir_changement_centre_extremes = models.IntegerField()
    class Meta:
        db_table = 'legislative_per_cir'

    def __str__(self):
        return f"{self.libelle_du_departement} - {self.code_de_la_circonscription}"