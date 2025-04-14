import pandas as pd

from django.db import models
from google.cloud import bigquery

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL,  
        null=True,  
        blank=True  
    )

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles') 

    def __str__(self):
        return self.title
    
class GeneratedImage(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.URLField(default="https://github.com/d-perreaux/OCR_initiation_machine_learning/blob/main/exo_01_regression_lineaire_simple/toto.png?raw=true")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} générée le {self.date_created}"

class ElectionDate(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)
    
class DataRequeteHTTP:
    @staticmethod
    def RequetHTTP():
        try:
            client = bigquery.Client.from_service_account_json("core/mspr-454808-baf9c7d409e4.json")
            
            # Requête BigQuery
            query = """
                SELECT *
                FROM `mspr-454808.Legislative.LEG_CIRC_T2_MERGE_DW`
            """
            query_job = client.query(query)
            df = query_job.to_dataframe()
            return df
        except Exception as e:
            print(f"Erreur lors de la requête BigQuery : {e}")
            return pd.DataFrame()
        
# Modèle pour récupérer la data
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