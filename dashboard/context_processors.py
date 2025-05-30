from django.db.models.functions import Left

from core.models import UnemploymentPerCir

DEPARTEMENTS = {
    "59": "NORD",
    "62": "PAS-DE-CALAIS",
    "60": "OISE",
    "80": "SOMME",
    "02": "AISNE"
}

def available_years(request):
    available_years = UnemploymentPerCir.objects.values_list('annee', flat=True).distinct().order_by('annee')
    return {'years_list': [data for data in available_years]}

def available_departements(request):
    available_departements = UnemploymentPerCir.objects.annotate(
    department=Left('code_circonscription', 2)
).values('department').distinct()
    print('Available departments: ')
    print([data for data in available_departements])
    return {
    'available_departements': [
        {"id": data["department"], "label": DEPARTEMENTS[data["department"]]}
        for data in available_departements
    ]
}

def current_path(request):
    print(f"Current path: {current_path}")
    return {'current_path': request.path}