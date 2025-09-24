from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password


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
            return redirect("login/")
        else:
            print(form.errors) 
            #messages.error(request, "Please correct the errors below.")
    else:
        form = PendingUserForm()

    return render(request, "register.html", {"form": form, "roles": roles, "companies": companies})




def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user is pending first
        if PendingUser.objects.filter(email=email).exists():
            messages.warning(request, "Your account is not activated yet.")
            return render(request, 'login.html')

        user = User_info.objects.filter(email=email).first()
        if not user:
            messages.error(request, "Invalid email")
            return render(request, 'login.html')
       
        # breakpoint()
        # Check password for active user
        if check_password(password, user.password):
            # User authenticated, render dashboard
            return render(request, 'base.html', {'user': user})
        else:
            messages.error(request, "Invalid password.")

    return render(request, 'login.html')



def Logout(request):
    request.session.flush()
    messages.success(request, "Successfully logged out!") 
    return redirect('login')

@login_required(login_url='login')
def Dashboard(request):
    return render(request,'base.html')


