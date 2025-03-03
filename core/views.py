from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from database.models import Zipcode, Language
from django.contrib.auth.models import User
from django.http import JsonResponse


def index(request):
    return render(request, "index.html")


@login_required
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

        if User.objects.filter(username=username).exists():
            return render(
                request, "register.html", {"error": "Username already exists"}
            )

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()

            surname = request.POST["surname"]
            name = request.POST["name"]
            phone_number = request.POST["phone_number"]
            address = request.POST["address"]
            zipcode_value = request.POST["zipcode"]
            language_values = request.POST.getlist("language")
            rating = request.POST.get("rating", None)
            image_url = request.POST.get("image_url", None)

            zipcode, _ = Zipcode.objects.get_or_create(zipcode=zipcode_value)

            profile = Profile(
                user=user,
                user_type=user_type,
                surname=surname,
                name=name,
                phone_number=phone_number,
                address=address,
                zipcode=zipcode,
                rating=rating,
                image_url=image_url,
            )
            profile.save()

            for language_value in language_values:
                language, _ = Language.objects.get_or_create(language=language_value)
                profile.language.add(language)

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")

        except IntegrityError:
            return render(
                request,
                "register.html",
                {"error": "An error occurred. Please try again."},
            )

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
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "account.html", {"user": request.user})


@login_required
def bookings(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "bookings.html")


def get_languages(request):
    languages = Language.objects.all().values_list("language", flat=True)
    return JsonResponse(list(languages), safe=False)
