from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from database.models import Staff, Zipcode, Language, Customer
from django.contrib.auth.models import User


def index(request):
    return render(request, "index.html")


def staff_list(request):
    date = request.GET.get("date")
    time = request.GET.get("time")
    staff_list = Staff.objects.all()
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
        user_type = request.POST["user_type"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        user = User.objects.create_user(username=username, password=password)
        user.save()

        if user_type == "customer":
            surname = request.POST["surname"]
            name = request.POST["name"]
            phone_number = request.POST["phone_number"]
            address = request.POST["address"]
            zipcode_value = request.POST["zipcode"]
            language_value = request.POST["language"]

            zipcode, _ = Zipcode.objects.get_or_create(zipcode=zipcode_value)
            language, _ = Language.objects.get_or_create(language=language_value)

            customer = Customer(
                surname=surname,
                name=name,
                email=username,
                password=password,
                phone_number=phone_number,
                address=address,
                zipcode=zipcode,
                language=language,
            )
            customer.save()

        elif user_type == "staff":
            surname = request.POST["surname"]
            name = request.POST["name"]
            phone = request.POST["phone"]
            rating = request.POST.get("rating", None)
            zipcode_value = request.POST["zipcode"]
            language_value = request.POST["language"]
            image_url = request.POST["image_url"]

            zipcode, _ = Zipcode.objects.get_or_create(zipcode=zipcode_value)
            language, _ = Language.objects.get_or_create(language=language_value)

            staff = Staff(
                surname=surname,
                name=name,
                phone=phone,
                password=password,
                rating=rating,
                zipcode=zipcode,
                language=language,
                image_url=image_url,
            )
            staff.save()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")

    return render(request, "register.html")


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
    return render(request, "account.html", {"user": request.user})


@login_required
def bookings(request):
    return render(request, "bookings.html")
