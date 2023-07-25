from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()

    if request.user.is_authenticated:
        return render(request, 'home.html', {'records':records})
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
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered !!! Welcome !!!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    
    return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record':customer_record})
    else:
        messages.success(request, "You must be logged in !!!")
        return redirect('login')
    
def delete_customer_record(request, pk):
    if request.user.is_authenticated:
        # look up records
        customer_record = Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request, "Record have been deleted !!!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in !!!")
        return redirect('login')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added ...")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in !!!")
        return redirect('login') 
    
def update_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=customer_record)

        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record has been updated")
                return redirect('home') 
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in !!!")
        return redirect('login') 


    
    


