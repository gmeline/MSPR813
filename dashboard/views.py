import io
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import geopandas as gpd
from core.models import CriminalityPerCir, LegislativePerCir, UnemploymentPerCir, DensityPopulation, Prediction2027
import matplotlib.pyplot as plt
import base64
import cartopy.crs as ccrs
from django.shortcuts import render
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt

import geopandas as gpd
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os

def createHeatMap(df, type, title, filename="heatmap.png"):
    # Load geojson
    geo_df = gpd.read_file("https://france-geojson.gregoiredavid.fr/repo/regions/hauts-de-france/arrondissements-hauts-de-france.geojson")

    # Merge with user-provided data
    dfMerged = geo_df.merge(df, left_on="code", right_on="code_de_la_circonscription", how="left")
    projection = gcrs.AlbersEqualArea()

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': projection})

    # Draw choropleth
    gplt.choropleth(
        dfMerged,
        projection=projection,
        hue=type,
        cmap="viridis",
        scheme="quantiles",
        linewidth=0.5,
        edgecolor="black",
        legend=True,
        ax=ax
    )

    # Add labels
    for idx, row in dfMerged.iterrows():
        if row['geometry'] is not None and not row['geometry'].is_empty:
            x, y = row['geometry'].centroid.coords[0]
            ax.text(
                x, y,
                str(row['code']),
                fontsize=5,
                color='white',
                fontweight='bold',
                ha='center',
                va='center',
                transform=ccrs.PlateCarree()
            )

    plt.title(title)

    # Ensure the output directory exists
    os.makedirs("dashboard/static/img", exist_ok=True)

    # Construct full file path
    full_path = os.path.join("dashboard/static/img", filename)

    # Save the figure
    plt.savefig(full_path, format="png", bbox_inches="tight")
    plt.close(fig)

    print(f"Heatmap saved to: {full_path}")



def instabiliteSanCentre():
    predicitons_2027 = Prediction2027.objects.values("code_de_la_circonscription", "instabilite_sans_centre")
    df = pd.DataFrame(list(predicitons_2027))
    return createHeatMap(df, "instabilite_sans_centre", "Instabilité sans centre par circonscription", 'instabilite_sans_centre.png')

def desirChangementSansCentre():
    predicitons_2027 = Prediction2027.objects.values("code_de_la_circonscription", "desir_changement_sans_centre")
    df = pd.DataFrame(list(predicitons_2027))
    return createHeatMap(df, "desir_changement_sans_centre", "Desir de changement sans centre par circonscription", 'desir_changement_sans_centre.png')

def instabiliteAvecCentre():
    predicitons_2027 = Prediction2027.objects.values("code_de_la_circonscription", "instabilite_avec_centre")
    df = pd.DataFrame(list(predicitons_2027))
    return createHeatMap(df, "instabilite_avec_centre", "Instabilité avec centre par circonscription", "instabilite_avec_centre.png")

def desirChangementAvecCentre():
    predicitons_2027 = Prediction2027.objects.values("code_de_la_circonscription", "desir_changement_avec_centre")
    df = pd.DataFrame(list(predicitons_2027))
    return createHeatMap(df, "desir_changement_avec_centre", "Desir de changement avec centre par circonscription", "desir_changement_avec_centre.png")

def desirChangementAvecExtremeCentre():
    predicitons_2027 = Prediction2027.objects.values("code_de_la_circonscription", "desir_changement_centre_extremes")
    df = pd.DataFrame(list(predicitons_2027))
    return createHeatMap(df, "desir_changement_centre_extremes", "Desir de changement avec centre extreme par circonscription", "desir_changement_centre_extremes.png")

def instabiliteAvecExtremeCentre():
    predicitons_2027 = Prediction2027.objects.values("code_de_la_circonscription", "instabilite_centre_extremes")
    df = pd.DataFrame(list(predicitons_2027))
    return createHeatMap(df, "instabilite_centre_extremes", "Instabilité avec centre extreme par circonscription", "instabilite_centre_extremes.png")

# VIEWS.
def dashboard(request):
    # criminally_data = generate_graph()
    available_years = UnemploymentPerCir.objects.values_list('annees', flat=True).distinct()
    return render(request, 'dashboard/index.html', {'available_years': available_years})

def travail(request):
    return render(request, 'dashboard/travail/travail.html', {'resultSanCentre': ["instabilite_sans_centre.png", "desir_changement_sans_centre.png"], 'resultAvecCentre': ["instabilite_avec_centre.png", "desir_changement_avec_centre.png"], 'resultAvecCentreExtreme': ["desir_changement_centre_extremes.png", "instabilite_centre_extremes.png"]})

def criminality(request):
    return render(request, 'dashboard/criminality/index.html', {"graphs": ["sankey_diagram_previous_shade_avec_centre.html", "sankey_diagram_previous_shade_centre_extremes.html", "sankey_diagram_previous_shade_sans_centre.html"]})
