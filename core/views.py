from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from database.forms import UserRegisterForm
from database.models import CustomUser, Language
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from database.models import Booking
import json
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def index(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.user_type == "staff":
            pending_bookings = Booking.objects.filter(
                staff=request.user, status="pending"
            ).order_by("date", "time")

            confirmed_bookings = Booking.objects.filter(
                staff=request.user, status="confirmed", date__gte=timezone.now().date()
            ).order_by("date", "time")

            context.update(
                {
                    "pending_bookings": pending_bookings,
                    "confirmed_bookings": confirmed_bookings,
                }
            )
        else:
            # Add bookings for customers
            bookings = Booking.objects.filter(customer=request.user).order_by(
                "-date", "-time"
            )
            context["bookings"] = bookings

    return render(request, "index.html", context)


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
        admin_password = request.POST.get("admin_password")
        if admin_password != settings.ADMIN_REGISTRATION_PASSWORD:
            messages.error(
                request, "Invalid admin password. Please contact an administrator."
            )
            return render(request, "register.html", {"error": "Invalid admin password"})

        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("index")
    else:
        form = UserRegisterForm()

    languages = Language.objects.all().order_by("name")
    return render(request, "register.html", {"form": form, "languages": languages})


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
        if request.FILES.get("profile_picture"):
            file = request.FILES["profile_picture"]

            # Validate file type
            if not file.content_type.startswith("image/"):
                messages.error(request, "Invalid file type. Please upload an image.")
                return redirect("account")

            # Delete old picture if it exists
            if request.user.picture:
                request.user.picture.delete(save=False)

            request.user.picture = file

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
@require_http_methods(["POST"])
def create_booking(request):
    try:
        data = json.loads(request.body)
        booking = Booking.objects.create(
            customer=request.user,
            staff_id=data["staff_id"],
            date=data["date"],
            time=data["time"],
            address=data["address"],
            status="pending",
        )
        return JsonResponse({"status": "success", "booking_id": booking.id})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@login_required
def bookings(request):
    if request.user.user_type == "customer":
        user_bookings = Booking.objects.filter(customer=request.user)
    else:
        # For staff, show all bookings with pending first
        user_bookings = Booking.objects.filter(staff=request.user).order_by(
            models.Case(models.When(status="pending", then=0), default=1),
            "-date",
            "-time",
        )
    return render(request, "bookings.html", {"bookings": user_bookings})


@login_required
@require_http_methods(["GET"])
def get_user_profile(request):
    user = request.user
    return JsonResponse(
        {
            "street": user.street,
            "street_number": user.street_number,
            "apartment": user.apartment,
            "city": user.city,
            "state": user.state,
            "zip_code": user.zip_code,
            "country": user.country,
        }
    )


@login_required
@require_http_methods(["POST"])
def update_booking_status(request, booking_id):
    try:
        data = json.loads(request.body)
        booking = Booking.objects.get(id=booking_id)

        # Only staff can update booking status
        if request.user.user_type != "staff" or booking.staff != request.user:
            return JsonResponse(
                {"status": "error", "message": "Unauthorized"}, status=403
            )

        # Validate the status
        valid_statuses = ["confirmed", "cancelled"]
        if data["status"] not in valid_statuses:
            return JsonResponse(
                {"status": "error", "message": "Invalid status"}, status=400
            )

        # Update the booking status
        booking.status = data["status"]
        booking.save()

        # Return success response with updated booking info
        return JsonResponse(
            {
                "status": "success",
                "booking_id": booking.id,
                "new_status": booking.status,
                "message": f"Booking {booking.status} successfully",
            }
        )
    except Booking.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Booking not found"}, status=404
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@csrf_exempt  # Allow requests without CSRF token
@require_http_methods(["GET"])
def health_check(request):
    from django.db import connection

    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        # Test CSRF token generation
        from django.middleware.csrf import get_token

        get_token(request)

        # Test static file handling
        from django.contrib.staticfiles.finders import get_finder

        finder = get_finder("django.contrib.staticfiles.finders.FileSystemFinder")
        if not finder.find("css/styles.css"):
            raise Exception("Static files not properly configured")

        return JsonResponse(
            {"status": "healthy", "database": "connected", "static_files": "configured"}
        )
    except Exception as e:
        return JsonResponse(
            {
                "status": "unhealthy",
                "error": str(e),
                "database": (
                    "not connected" if "cursor" not in locals() else "connected"
                ),
                "static_files": (
                    "not configured" if "finder" not in locals() else "configured"
                ),
            },
            status=500,
        )


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been successfully deleted.")
        return redirect("index")
    return redirect("account")
