from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'main_app/index.html')

def register(request):
    response = User.objects.add_user(request.POST)
    if response['status']:
        # successfully added user
        request.session['user_id'] = response['new_user'].id
        request.session['user_fname'] = response['new_user'].first_name
        request.session['user_lname'] = response['new_user'].last_name
        return redirect('success')
    else:
        # failed validations
        for error in response['errors']:
            messages.error(request, error)
        return redirect('index')

def login(request):
    response = User.objects.check_user(request.POST)
    if response['status']:
        # successfully logged in user
        request.session['user_id'] = response['loggedin_user'].id
        request.session['user_fname'] = response['loggedin_user'].first_name
        request.session['user_lname'] = response['loggedin_user'].last_name
        return redirect('success')
    else:
        # failed validations
        for error in response['errors']:
            messages.error(request, error)
        return redirect('index')

def logout(request):
    request.session.clear()
    return redirect('index')

def success(request):
    return render(request, 'main_app/success.html')
