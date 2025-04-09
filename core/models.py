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