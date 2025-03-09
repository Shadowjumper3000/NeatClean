from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from database.forms import UserRegisterForm
from database.models import Profile


def index(request):
    return render(request, "index.html")


@login_required
def staff_list(request):
    date = request.GET.get("date")
    time = request.GET.get("time")
    staff_list = Profile.objects.all()
    context = {
        "date": date,
        "time": time,
        "staff_list": staff_list,
    }
    return render(request, "staffList.html", context)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect("account")
            response.set_cookie("auth", "true", max_age=3600)  # Set cookie for 1 hour
            return response
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(
                user=user,
                user_type=form.cleaned_data['user_type'],
                city=form.cleaned_data['city'],
                zip=form.cleaned_data['zip'],
                street=form.cleaned_data['street'],
                address=form.cleaned_data['address'],
                apartment_door_floor=form.cleaned_data['apartment_door_floor'],
                phone_number=form.cleaned_data['phone_number'],
                languages=form.cleaned_data['languages'],
                rating=form.cleaned_data['rating'],
                image_url=form.cleaned_data['image_url']
            )
            profile.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Redirect to the home page after registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        response = redirect("index")
        response.delete_cookie("auth")  # Delete the auth cookie
        return response
    return redirect("index")


@login_required
def account(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "account.html", {"user": request.user})


@login_required
def bookings(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "bookings.html")

