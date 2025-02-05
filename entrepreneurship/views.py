from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


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


@login_required
def account(request):
    return render(request, "account.html", {"user": request.user})


@login_required
def bookings(request):  # Add this view for bookings
    return render(request, "bookings.html")