from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from .serializes import PendingUserSerializer, UserInfoSerializer

from .models import *
from .forms import PendingUserForm

# Create your views here.


def Register(request):
    roles = User_role.objects.all()
    companies = Company_info.objects.all()

    if request.method == "POST":
        serializer = PendingUserSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()  # saves pending user with hashed password
            messages.success(request, "User registered successfully and is pending approval.")
            return redirect("login/")  # redirect to login page
        else:
            print(serializer.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        serializer = PendingUserSerializer()

    return render(request, "register.html", {"form": serializer, "roles": roles, "companies": companies})





def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user is still pending
        if PendingUser.objects.filter(email=email).exists():
            messages.warning(request, "Your account is not activated yet.")
            return render(request, 'login.html')

        # Check active users
        user = User_info.objects.filter(email=email).first()
        if not user:
            messages.error(request, "Invalid email")
            return render(request, 'login.html')

        # Check password
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


