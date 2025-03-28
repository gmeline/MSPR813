from django.shortcuts import render


def exploration(request):
    return render(request, 'exploration/index.html')