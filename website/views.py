from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html', {})
    else:
        return redirect('login')

def login_user(request):
    # check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user:
                login(request, user)
                return redirect('home')
        else:
            messages.success(request, "There was an error logging in, Please try again...")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out ...")
    return redirect('home')
            
def register_user(request):
    return render(request, 'register.html', {})


