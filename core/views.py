from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static



def index(request):
    return render(request, "index.html")

def staff_list(request):
    date = request.GET.get('date')
    time = request.GET.get('time')
    #ex staff
    staff_list = [
        {'name': 'John Doe', 'image_url': static('img/image1.jpeg'), 'rating': 4.5},
        {'name': 'Jane Smith', 'image_url': 'path/to/image2.jpg', 'rating': 4.7},
    ]

    context = {
        'date': date,
        'time': time,
        'staff_list': staff_list,
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
