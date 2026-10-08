from lib2to3.fixes.fix_input import context
import pandas as pd
from django.core.exceptions import ValidationError
from .models import ChatMessage, RegistrationFile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Item
from .forms import MySignupForm, MyLogin, ItemForm, ProfileUpdateForm
from django.contrib.auth import login, authenticate, logout, get_backends
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
import smtplib
from django.views.generic import TemplateView
from email.mime.text import MIMEText
from django.contrib.auth import get_user_model
import logging
from django.contrib.auth import login as auth_login, logout as auth_logout


# Create your views here.

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# Set up logging
logger = logging.getLogger(__name__)
User = get_user_model()  # This will get the User model


def check_registration_number_exists(registration_number):
    try:
        # Fetch the latest uploaded file
        registration_file = RegistrationFile.objects.latest('uploaded_at')
        file_path = registration_file.file.path

        # Detect file type and load data
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            raise ValidationError("Unsupported file format. Please upload a CSV or Excel file.")

        # Ensure 'registration_number' column exists
        if 'registration_number' not in df.columns:
            raise ValidationError("The file does not contain a 'registration_number' column.")

        # Convert to string and check if the registration number exists
        registration_numbers = df['registration_number'].astype(str).tolist()
        return registration_number in registration_numbers

    except RegistrationFile.DoesNotExist:
        raise ValidationError("No registration file found. Please upload a file to continue.")
    except Exception as e:
        raise ValidationError(f"Error processing registration file: {e}")


def signup(request):
    if request.method == 'POST':
        form = MySignupForm(request.POST, request.FILES)
        if form.is_valid():
            registration_number = form.cleaned_data['registration_number']
            # Validate registration number
            if check_registration_number_exists(registration_number):
                # Save the user if registration number is valid
                user = form.save()
                return redirect('/login')
            else:
                form.add_error('registration_number', "Your registration number is not valid or not from LPU.")
    else:
        form = MySignupForm()

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = MyLogin(request.POST)
        if form.is_valid():
            registration_number = form.cleaned_data['registration_number']
            password = form.cleaned_data['password']

            # Authenticate the user using phoneNumber as username
            user = authenticate(request, username=registration_number, password=password)

            if user is not None:
                auth_login(request, user)  # Log the user in using the correct function
                print(f"User {user.username} logged in successfully.")
                return redirect('home')  # Redirect to home or another URL
            else:
                print("Invalid password or username.")
                return render(request, 'login.html', {'form': form, 'error': 'Invalid phone number or password'})
    else:
        form = MyLogin()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


@login_required
def submit_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()  # Save the item to the database
            print(f"Uploaded image: {item.image}")  # Log the image path
            return redirect('item_list')
        else:
            print(f"Form errors: {form.errors}")  # Log any form errors for debugging
    else:
        form = ItemForm()
    return render(request, 'submit_item.html', {'form': form})


# View to display all items in a list
def item_list(request):
    query = request.GET.get('q')
    if query:
        items = Item.objects.filter(item_name__icontains=query)
    else:
        items = Item.objects.all()

    context = {
        'items': items,
        'query': query
    }
    return render(request, 'item_list.html', context)


# View to display specific item details
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail.html', {'item': item})


@require_POST
def contact_owner(request, item_id):
    # Get the item based on the provided item_id
    item = get_object_or_404(Item, id=item_id)
    phone_number = request.POST.get('phone_number')

    # Prepare the email details
    subject = f"Customer Interested in {item.item_name}"
    message = (f"One customer is interested in your product: {item.item_name}. "
               f"Please contact them at this phone number: {phone_number}.")
    to_email = item.email  # Assuming the owner has an email field

    # Gmail SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    gmail_user = "email"  # Replace with your Gmail address
    gmail_password = "password"  # Replace with your Gmail password

    try:
        # Create the email
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = to_email

        # Connect to the Gmail SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(gmail_user, gmail_password)  # Login to your Gmail account
            server.sendmail(gmail_user, to_email, msg.as_string())  # Send the email

        # Provide feedback to the user
        messages.success(request, "Your message has been sent to the owner.")
    except Exception as e:
        # Handle any errors that occur during email sending
        messages.error(request, f"An error occurred while sending the email: {str(e)}")

    # Redirect back to the item detail page
    return redirect('item_detail', item_id=item_id)


@login_required
def community_chat(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        image = request.FILES.get('image')
        chat_message = ChatMessage(user=request.user, message=message, image=image)
        chat_message.save()
        return redirect('community_chat')

    chat_messages = ChatMessage.objects.all().order_by('-timestamp')
    return render(request, 'community_chat.html', {'chat_messages': chat_messages})


class LearnMoreView(TemplateView):
    template_name = 'learn_more.html'


def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        item.item_name = request.POST['item_name']
        item.item_description = request.POST['item_description']
        item.selling_price = request.POST['selling_price']

        # Handle image upload
        if request.FILES.get('image'):
            item.image = request.FILES['image']

        item.save()
        return redirect('item_list')

    context = {
        'item': item,
    }
    return render(request, 'edit_item.html', context)


def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        item.delete()
        return redirect('item_list')  # Redirect to item list after deletion

    return redirect('item_list')


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    items = Item.objects.filter(owner=request.user)

    if request.method == 'POST':
        # Use the ProfileUpdateForm for updates
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Ensure this matches your URL pattern name
    else:
        form = ProfileUpdateForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
        'items': items,
    }
    return render(request, 'profile.html', context)
