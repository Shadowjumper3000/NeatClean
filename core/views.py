from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, "index.html")

def staff_list(request):
    date = request.GET.get('date')
    time = request.GET.get('time')
    context = {
        'date': date,
        'time': time,
    }
    return render(request,"staffList.html", context)

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect("account")
            response.set_cookie("auth", "true", max_age=3600)
            return response
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("account")
        else:
            return render(
                request, "register.html", {"form": form, "error": form.errors}
            )
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


@login_required
def account(request):
    return render(request, "account.html", {"user": request.user})


@login_required
def bookings(request):
    return render(request, "bookings.html")
