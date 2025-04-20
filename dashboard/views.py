import pandas as pd
import squarify
from django.db.models.aggregates import Sum
from django.db.models.functions import Substr

from core.models import CriminalityPerCir, LegislativePerCir, UnemploymentPerCir, DensityPopulation
from core.testService import DataService
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.shortcuts import render


def generate_graph():
    # Query your data (example with SalesData model)
    criminally_data = CriminalityPerCir.objects.filter(annee='2019').all()

    # Extract the data to plot
    circuncription = [data.code_circonscription for data in criminally_data]
    crime_number = [data.nombre for data in criminally_data]
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(circuncription, crime_number, marker='o', linestyle='-', color='b')

    # Title and labels
    plt.title('Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # Close the plot to free up memory
    plt.close()

    return img_base64

def create_unemployment_radar_chart_image():
    print('GOGOOOO-s-----')
    unemployed_data = get_unemployment_data()
    print([data["total_nombre"] for data in unemployed_data])
    df = pd.DataFrame({'nb_people': [data["total_nombre"] for data in unemployed_data], 'group': [data["department"] for data in unemployed_data]})
    labels = [f"{name}\n{parent[5:]}\n{value}" for name, value, parent in zip(df['group'], df['nb_people'], df['group'])]
    # plot it
    squarify.plot(sizes=df['nb_people'], label=labels, alpha=.8)
    plt.axis('off')
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # Close the plot to free up memory
    plt.close()

    return img_base64

def get_election_result():
    election_result = LegislativePerCir.objects.all()
    election_data = [data.blancs_et_nuls for data in election_result]

def get_unemployment_data():
    unemplyment_result = CriminalityPerCir.objects.annotate(department=Substr('code_circonscription', 1, 2)).values('department').annotate(total_nombre=Sum('nombre')).order_by('department')
    return [data for data in unemplyment_result]
def get_densityPopulation_data():
    density_population_result = DensityPopulation.objects.all()
    densityt_data = [data.density for data in density_population_result]

# Create your views here.
def dashboard(request):
    criminally_data = generate_graph()
    image_data = create_unemployment_radar_chart_image()
    unemploy_daata = create_unemployment_radar_chart_image()
    get_unemployment_data()
    get_densityPopulation_data()
    return render(request, 'dashboard/index.html', {'criminally': criminally_data, 'unemployment_data': unemploy_daata})

def travail(request):
    return render(request, 'dashboard/travail/travail.html')

def criminality(request):


    return render(request, 'dashboard/criminality/index.html')

def elections(request):
    return render(request, 'dashboard/elections/index.html')