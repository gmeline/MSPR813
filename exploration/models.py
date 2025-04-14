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

    def __str__(self):
        return f"{self.libelle_du_departement} - {self.code_de_la_circonscription}"