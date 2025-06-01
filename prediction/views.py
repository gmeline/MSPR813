from django.shortcuts import render
import joblib
import os
from core.models import Prediction2027, DensityPopulation

# Create your views here.
def choix(request):
    return render(request, 'choix/index.html')

def prediction(request):
    prediction_result = None
    params_utilises = {}

    if request.method == 'POST':
        code_dept = request.POST.get('code_departement')
        num_circo = request.POST.get('numero_circonscription')
        insecurite = request.POST.get('insecurite')

        try:
            insecurite = float(insecurite)


            num_circo_formate = str(num_circo).zfill(3)
            code_circo = f"{code_dept}{num_circo_formate}"


            pred_data = Prediction2027.objects.get(code_de_la_circonscription=code_circo)
            precedent = float(pred_data.encodage_avec_centre_gagnant_precedent)
            instabilite = float(pred_data.instabilite_centre_extremes)
            poids_nuance = float(pred_data.poids_nuance_centre_extremes)
            desir_changement = float(pred_data.desir_changement_centre_extremes)


            density_data = DensityPopulation.objects.filter(code_departement=code_dept).first()
            densite = float(density_data.density)

            data = [[
                precedent,
                insecurite,
                0.0,  
                densite,
                instabilite,
                poids_nuance,
                desir_changement
            ]]

            model_path = os.path.join("prediction", "model_with_center_previous_instability_criminality_unemployment_density")
            model = joblib.load(model_path)
            prediction_result = model.predict(data)[0]

            label_result = {1: "Gauche", 2: "Centre", 3: "Droite"}.get(prediction_result, "Inconnu")

            params_utilises = {
                'code_circo': code_circo,
                'encodage_sans_centre_gagnant_precedent': precedent,
                'insecurite': insecurite,
                'densite': densite,
                'instabilite_centre_extremes': instabilite,
                'poids_nuance_centre_extremes': poids_nuance,
                'desir_changement_centre_extremes': desir_changement,
                'prediction_label': label_result
            }

        except Prediction2027.DoesNotExist:
            prediction_result = "Circonscription inconnue."
        except ValueError:
            prediction_result = "Veuillez entrer des valeurs valides."
        except Exception as e:
            prediction_result = f"Erreur : {str(e)}"

    return render(request, 'prediction_m1/index.html', {
        'prediction': prediction_result,
        'params_utilises': params_utilises
    })