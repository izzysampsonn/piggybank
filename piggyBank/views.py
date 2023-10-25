from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')  # Render the home.html template


def piggy_bank(request):
    return render(request, 'piggybank.html')
