from django.shortcuts import render
import joblib
import os

# Create your views here.
def choix(request):
    return render(request, 'choix/index.html')

def prediction(request):
    prediction_result = None
    if request.method == 'POST':
        data = [[
            float(request.POST.get('precedent')),
            float(request.POST.get('tauxpourmille')),
            float(request.POST.get('tauxdechomage')),
            float(request.POST.get('densite')),
            float(request.POST.get('instabilitecentreextreme')),
            float(request.POST.get('poidsnuancecentreextremes')),
            float(request.POST.get('desirchangementcentreextremes')),
        ]]
        model_path = os.path.join("prediction", "model_with_center_previous_instability_criminality_unemployment_density")
        model = joblib.load(model_path)
        prediction_result = model.predict(data)[0]
    return render(request, 'prediction/index.html', {'prediction': prediction_result})