import os

import numpy as np
import pandas as pd
import squarify
from django.conf import settings
from django.db.models.aggregates import Sum, Avg
from django.db.models.functions import Substr, Left
import matplotlib
matplotlib.use('Agg')
from core.models import CriminalityPerCir, LegislativePerCir, UnemploymentPerCir, DensityPopulation
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.shortcuts import render

DEPARTEMENTS = {
    "59": "NORD",
    "62": "PAS-DE-CALAIS",
    "60": "OISE",
    "80": "SOMME",
    "02": "AISNE"
}

# Graphs
def create_tree_map(values, labels, title=''):
    df = pd.DataFrame({'values': values, 'labels': labels})
    df['label'] = df.apply(lambda row: f"{row['labels']}\n{row['values']:,}", axis=1)
    # plot it
    fig, ax = plt.subplots()
    squarify.plot(sizes=df['values'], label=df['label'], alpha=.8)
    ax.axis('off')
    plt.title(title)
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    ax.margins(0, 0)  # Further reduce margins
    fig.tight_layout(pad=0)
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # Close the plot to free up memory
    plt.close()

    return img_base64

def create_bar_chart(values, labels, title = '', ylabel=''):
    names = labels
    values = values
    # Label distance: gives the space between labels and the center of the pie
    y_pos = np.arange(len(names))

    # Create bars
    plt.bar(y_pos, values)
    plt.ylabel(ylabel)
    plt.title(title)
    # Create names on the x-axis
    plt.xticks(y_pos, names)

    # Show graphic
    img = BytesIO()
    plt.xticks(rotation=45, ha='right')
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    # static_img_path = os.path.join(settings.BASE_DIR, 'dashboard', 'static', 'dashboard', 'img')
    # if not os.path.exists(static_img_path):
    #     os.makedirs(static_img_path)
    #
    #     # Construct the full file path
    # filepath = os.path.join(static_img_path, 'bar_chart.png')
    # print("Saving image to {}".format(filepath))
    # # Save the figure
    # plt.savefig(filepath, format='png', bbox_inches='tight', pad_inches=0)
    # Close the plot to free up memory
    plt.close()

    return img_base64

def create_lolipop_chart(labels, values, title = '', ylabel=''):
    print("Density population")
    print(values)
    plt.ylabel(ylabel)  # Update the y-axis label
    plt.title(title)

    plt.stem(labels, values)
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # Close the plot to free up memory
    plt.close()

    return img_base64


# Graph Builders
def cheumeurs_par_departement(year=2014):
    unemployed_data = UnemploymentPerCir.objects.filter(annee=year).annotate(
        department=Left('code_circonscription', 2)
    ).values('department').annotate(
        total_nombre=Sum('chomeurs')
    ).order_by('department')

    return create_tree_map([data["total_nombre"] for data in unemployed_data],  [DEPARTEMENTS[data["department"]] for data in unemployed_data], f'Cheumeurs par departament in %s' % year)

def avg_chomage(year=2014):
    taux_chomage =   UnemploymentPerCir.objects.filter(annee=year).annotate(
        department=Left('code_circonscription', 2)
    ).values('department').annotate(
        taux_chomage=Avg('taux_chomage')
    ).order_by('department')
    names = [data["taux_chomage"] for data in taux_chomage]
    values = mapDepartement(taux_chomage)
    return create_bar_chart(names, values, f'Average Taux de chommeurs par departement en %s' % year, 'Average (Percentage)')

def population_density(year=2014):
    print("Population density", year)
    population = UnemploymentPerCir.objects.filter(annee=year).annotate(
        department=Left('code_circonscription', 2)
    ).values('department').annotate(
        population=Sum('populationauth_groupunemployment_per_cir')
    ).order_by('department')
    names = mapDepartement(population)
    values = [data["population"] for data in population]
    return create_lolipop_chart(names, values, f'Population par departement en %s' %year, 'Population (Millions)')


def get_election_result():
    election_result = LegislativePerCir.objects.all()
    election_data = [data.blancs_et_nuls for data in election_result]

def get_unemployment_data_59_2014():
    """
    Retrieves code_circonscription and taux_chomage for year 2014,
    where code_circonscription starts with '59'.
    """
    unemployment_data = UnemploymentPerCir.objects.filter(
        code_circonscription__startswith='59',
        annee=2014
    ).values('code_circonscription', 'taux_chomage')

    # Convert the QuerySet to a list of dictionaries for easier use in templates
    names = [data["code_circonscription"] for data in unemployment_data]
    values = [data["taux_chomage"] for data in unemployment_data]
    return create_bar_chart(values, names, f'Taux de chommage par circonscription en %s' % 2014, 'Average (Percentage)')

def get_unemployment_data_59_2014():
    unemployment_data = UnemploymentPerCir.objects.filter(
        code_circonscription__startswith='59',
        annee=2014
    ).values('code_circonscription', 'taux_chomage')

    # Convert the QuerySet to a list of dictionaries for easier use in templates
    names = [data["code_circonscription"] for data in unemployment_data]
    values = [data["taux_chomage"] for data in unemployment_data]
    return create_bar_chart(values, names, f'Taux de chommage par circonscription en %s' % 2014, 'Average (Percentage)')

def get_unemployment_data_59_2014_chomeurs():
    unemployment_data = UnemploymentPerCir.objects.filter(
        code_circonscription__startswith='59',
        annee=2014
    ).values('code_circonscription', 'chomeurs')

    # Convert the QuerySet to a list of dictionaries for easier use in templates
    names = [data["code_circonscription"] for data in unemployment_data]
    values = [data["chomeurs"] for data in unemployment_data]
    return create_lolipop_chart(names, values, f'Taux de chommage par circonscription en %s' % 2014, 'Average (Percentage)')
#
# def createGraphAvgCHomage():
#     taux_chomage = getAvgChomage()
#     names = mapDepartement(taux_chomage)
#     values = [data["taux_chomage"] for data in taux_chomage]
#
#     print([data["taux_chomage"] for data in taux_chomage])
#     # Label distance: gives the space between labels and the center of the pie
#     y_pos = np.arange(len(names))
#
#     # Create bars
#     plt.bar(y_pos, values)
#
#     # Create names on the x-axis
#     plt.xticks(y_pos, names)
#
#     # Show graphic
#     img = BytesIO()
#     plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
#     img.seek(0)
#     img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
#
#     # Close the plot to free up memory
#     plt.close()
#
#     return img_base64
#
# def createGraphPopulation():
#     population = getPopulation()
#     names = mapDepartement( population)
#     values = [data["taux_chomage"] for data in population]
#
#     print([data["taux_chomage"] for data in population])
#     # Label distance: gives the space between labels and the center of the pie
#     y_pos = np.arange(len(names))
#
#     # Create bars
#     plt.bar(y_pos, values)
#
#     # Create names on the x-axis
#     plt.xticks(y_pos, names)
#
#     # Show graphic
#     plt.show()
#     img = BytesIO()
#     plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
#     img.seek(0)
#     img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
#
#     # Close the plot to free up memory
#     plt.close()
#
#     return img_base64

# def get_densityPopulation_data():
#     density_population_result = DensityPopulation.objects.all()
#     densityt_data = [data.density for data in density_population_result]



# VIEWS.
def dashboard(request):
    # criminally_data = generate_graph()
    available_years = UnemploymentPerCir.objects.values_list('annees', flat=True).distinct()
    print('Available years: ')
    print([data["population"] for data in available_years])
    return render(request, 'dashboard/index.html', {'available_years': available_years})

def travail(request):
    year = request.GET.get('years')
    departement = request.GET.get('department')

    if year or departement :
        return render(request, 'dashboard/travail/travail.html', {'unemployed_data': cheumeurs_par_departement(year), 'taux_chomage': avg_chomage(year), 'population': population_density(year)})

    return render(request, 'dashboard/travail/travail.html', {'unemployed_data': cheumeurs_par_departement, 'taux_chomage': avg_chomage(), 'population': population_density, 'taux_chomage_59': get_unemployment_data_59_2014, 'chomeurs': get_unemployment_data_59_2014_chomeurs})

def criminality(request):
    return render(request, 'dashboard/criminality/index.html')

def elections(request):
    return render(request, 'dashboard/elections/index.html')

# Outils
def mapDepartement(datatoMap):
    return [DEPARTEMENTS[data["department"]] for data in datatoMap]