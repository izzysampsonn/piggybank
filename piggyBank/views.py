from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
import io

# Create your views here.
# Initialize global variables for transactions and current balance
transactions = []
current_balance = 0
# Initialize a global goal array to store goal objects
goals = []
username = ''
age = 0

def home(request):
    return render(request, 'home.html', {'username': username})  # Render the home.html template


def track_allowance(request):
    # Use the global variables
    global transactions, current_balance, goals, age

    if request.method == 'POST':
        amount = int(request.POST.get('amount'))
        action = request.POST.get('action')  # 'deposit' or 'withdraw'

        # Determine if it's a deposit or withdrawal and update the transactions list and current balance
        if action == 'deposit':
            if int(age) < 10:
                action_text = 'added'
            else:
                action_text = 'deposited'
        else:
            if int(age) < 10:
                action_text = 'took away'
            else:
                action_text = 'withdrew'

        transactions.append(f'You {action_text} ${amount} dollars.')

        if action == 'deposit':
            current_balance += amount
        elif action == 'withdraw':
            if amount > current_balance:
                return render(request, 'allowance_tracker.html', {'current_balance': current_balance, 'transactions': transactions, 'error_message': 'Insufficient funds!', 'goals': goals, 'age': age, 'username': username})
            current_balance -= amount

        # Update progress bars for goals after form submission
        for goal in goals:
            if current_balance >= goal['amount']:
                goal['progress'] = 100
            else:
                goal['progress'] = (current_balance / goal['amount']) * 100

    # Pass the current balance, transactions list, and updated goals array to the template
    return render(request, 'allowance_tracker.html', {'current_balance': current_balance, 'transactions': transactions, 'goals': goals, 'age': age, 'username': username})


def goal_list(request):
    # Logic to retrieve and pass current goals to the template
    goals = []  # Replace this with logic to fetch goals from your database or storage
    return render(request, 'goal_list.html', {'goals': goals})


def goal_form(request):
    return render(request, 'add_Goals.html', {'username': username})


def save_goal(request):
    if request.method == 'POST':
        item_name = request.POST.get('itemName')
        item_price = int(request.POST.get('itemPrice'))
        item_image = request.FILES.get('itemImage')  # Get the uploaded file

        # Check if an image was uploaded
        if item_image:
            # Read the uploaded file into memory
            img_content = item_image.read()
            # Create an InMemoryUploadedFile object from the content
            img_io = io.BytesIO(img_content)
            img_file = InMemoryUploadedFile(
                img_io, None, item_image.name, item_image.content_type, len(img_content), None)

            # Convert the image file to base64 for storage
            base64_image = base64.b64encode(img_file.read()).decode('utf-8')

        # Create a new goal object based on the submitted data
        goal = {
            'description': item_name,
            'amount': item_price,
            'progress': 0,  # Initialize progress to 0, indicating no progress made yet
            # Store the base64 image, or None if no image was uploaded
            'image': base64_image if item_image else None
        }

        if current_balance > 0:
            goal['progress'] = round((current_balance / goal['amount']) * 100, 2)

        # Add the new goal to the global goals array
        goals.append(goal)

    # Redirect to the allowance tracker page
    return render(request, 'allowance_tracker.html', {'current_balance': current_balance, 'transactions': transactions, 'goals': goals, 'age': age, 'username': username})


def signin(request):
    global username, age
    if request.method == 'POST':
        username = request.POST.get('username')
        age = request.POST.get('age')
        # Redirect to the home page and pass the username as context
        return render(request, 'home.html', {'username': username})
    else:
        return render(request, 'signin.html')


def signout(request):
    global username, age
    # Clear the username to sign the user out
    username = ""
    age = 0
    # Redirect to the home page
    return render(request, 'home.html')
