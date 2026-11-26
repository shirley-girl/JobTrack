from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import UserProfile
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django. contrib  import messages
# Create your views here.
def get_started(request):
    return HttpResponse("<h2> Welcome to your page</h2>")

def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    else:
        form = UserCreationForm()

    # Apply Bootstrap styling to form fields
    for field in form.fields.values():
        field.widget.attrs.update({
            'class': 'form-control',
            'placeholder': f'Enter {field.label.lower()}'
        })

    if request.method == 'POST' and form.is_valid():

        with transaction.atomic():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)

        return redirect('dashboard')

    return render(request, 'account/register.html', {'form': form})

#login a user
def user_login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
    else:
        form = AuthenticationForm()

    # Apply Bootstrap styling to form fields
    for field in form.fields.values():
        field.widget.attrs.update({
            'class': 'form-control',
            'placeholder': f'Enter {field.label.lower()}'
        })

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'account/login.html', {'form': form})

# logout a user

def user_logout(request):
    if request.method == 'POST':
        
        logout(request)
        messages.info(request,"you've been logged out")
        return redirect('login')
    return redirect('dashboard')