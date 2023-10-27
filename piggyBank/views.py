from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.http import JsonResponse
from io import BytesIO
import json

# Create your views here.


def home(request):
    return render(request, 'home.html')  # Render the home.html template


transactions = []


def track_allowance(request):
    global transactions  # Use the global transactions list

    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        action = request.POST.get('action')  # 'deposit' or 'withdraw'

        # Determine if it's a deposit or withdrawal and update the transactions list
        if action == 'deposit':
            transactions.append(f'You deposited ${amount} dollars.')
        elif action == 'withdraw':
            transactions.append(f'You withdrew ${amount} dollars.')

    # Pass the transactions list to the template
    return render(request, 'allowance_tracker.html', {'transactions': transactions})
