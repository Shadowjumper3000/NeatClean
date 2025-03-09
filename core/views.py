from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from database.forms import UserRegisterForm
from database.models import CustomUser


def index(request):
    return render(request, "index.html")


@login_required
def staff_list(request):
    date = request.GET.get("date")
    time = request.GET.get("time")
    staff_list = CustomUser.objects.filter(
        user_type="staff"
    )  # Change to filter CustomUser
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
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("index")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


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
    if request.method == "POST":
        user = request.user
        # Update user information
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.phone = request.POST.get("phone")
        user.street = request.POST.get("street")
        user.street_number = request.POST.get("street_number")
        user.apartment = request.POST.get("apartment")
        user.city = request.POST.get("city")
        user.state = request.POST.get("state")
        user.zip_code = request.POST.get("zip_code")
        user.country = request.POST.get("country")

        # Handle profile picture upload
        if request.FILES.get("profile_picture"):
            user.picture = request.FILES["profile_picture"]

        user.save()
        messages.success(request, "Your profile has been updated successfully!")
        return redirect("account")

    return render(request, "account.html", {"user": request.user})


@login_required
def bookings(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "bookings.html")
