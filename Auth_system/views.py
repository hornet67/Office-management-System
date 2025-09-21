from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password


from .models import *
from .forms import PendingUserForm

# Create your views here.

def Register(request):
    roles = User_role.objects.all()
    companies = Company_info.objects.all()

    if request.method == "POST":
        form = PendingUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            messages.success(request, "User registered successfully and is pending approval.")
            return redirect("dashboard/")
        else:
            print(form.errors) 
            #messages.error(request, "Please correct the errors below.")
    else:
        form = PendingUserForm()

    return render(request, "register.html", {"form": form, "roles": roles, "companies": companies})


    

def Login(request):
    return render(request,'login.html')

def Dashboard(request):
    return render(request,'base.html')
