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


# Initialize global variables for transactions and current balance
transactions = []
current_balance = 0


def track_allowance(request):
    # Use the global transactions and current_balance variables
    global transactions, current_balance

    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        action = request.POST.get('action')  # 'deposit' or 'withdraw'

        # Determine if it's a deposit or withdrawal and update the transactions list and current balance
        if action == 'deposit':
            transactions.append(f'You deposited ${amount} dollars.')
            current_balance += amount
        elif action == 'withdraw':
            if amount > current_balance:
                return render(request, 'allowance_tracker.html', {'current_balance': current_balance, 'transactions': transactions, 'error_message': 'Insufficient funds!'})
            transactions.append(f'You withdrew ${amount} dollars.')
            current_balance -= amount

    # Pass the current balance and transactions list to the template
    return render(request, 'allowance_tracker.html', {'current_balance': current_balance, 'transactions': transactions})


def goal_list(request):
    # Logic to retrieve and pass current goals to the template
    goals = []  # Replace this with logic to fetch goals from your database or storage
    return render(request, 'goal_list.html', {'goals': goals})


def goal_form(request):
    return render(request, 'add_Goals.html')


def save_goal(request):
    # Logic to save the submitted goal data to your database or storage
    # Redirect the user to the goals page after saving the goal
    return render('goal_list')
