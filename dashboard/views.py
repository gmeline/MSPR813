from django.shortcuts import render

from core.models import CriminalityPerCir
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
    print(circuncription)
    print(crime_number)
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(circuncription, crime_numbelr, marker='o', linestyle='-', color='b')

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


# Create your views here.
def dashboard(request):
    criminally_data = generate_graph()
    return render(request, 'dashboard/index.html', {'criminally': criminally_data})