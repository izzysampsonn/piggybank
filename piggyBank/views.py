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
# Initialize a global goal array to store goal objects
goals = []


def track_allowance(request):
    # Use the global variables
    global transactions, current_balance, goals

    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        action = request.POST.get('action')  # 'deposit' or 'withdraw'

        # Determine if it's a deposit or withdrawal and update the transactions list and current balance
        if action == 'deposit':
            transactions.append(f'You deposited ${amount} dollars.')
            current_balance += amount
        elif action == 'withdraw':
            if amount > current_balance:
                return render(request, 'allowance_tracker.html', {'current_balance': current_balance, 'transactions': transactions, 'error_message': 'Insufficient funds!', 'goals': goals})
            transactions.append(f'You withdrew ${amount} dollars.')
            current_balance -= amount

        # Update progress bars for goals after form submission
        for goal in goals:
            if current_balance >= goal['amount']:
                goal['progress'] = 100
            else:
                goal['progress'] = (current_balance / goal['amount']) * 100

    # Pass the current balance, transactions list, and updated goals array to the template
    return render(request, 'allowance_tracker.html', {'current_balance': current_balance, 'transactions': transactions, 'goals': goals})


def goal_list(request):
    # Logic to retrieve and pass current goals to the template
    goals = []  # Replace this with logic to fetch goals from your database or storage
    return render(request, 'goal_list.html', {'goals': goals})


def goal_form(request):
    return render(request, 'add_Goals.html')


def save_goal(request):
    if request.method == 'POST':
        item_name = request.POST.get('itemName')
        item_price = int(request.POST.get('itemPrice'))

        # Create a new goal object based on the submitted data
        goal = {
            'description': item_name,
            'amount': item_price,
            'progress': 0  # Initialize progress to 0, indicating no progress made yet
        }
        if current_balance > 0:
            goal['progress'] = (current_balance/goal['amount']) * 100
        # Add the new goal to the global goals array
        goals.append(goal)

    # Redirect to the allowance tracker page (or goal list page)
        return render(request, 'add_Goals.html')
