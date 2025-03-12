"""
URL configuration for entrepreneurship project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    index,
    login_view,
    register_view,
    account,
    bookings,
    staff_list,
    logout_view,
    create_booking,
    get_user_profile,
    update_booking_status,
    health_check,
    delete_account,
)

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", index, name="index"),
        path("bookings/", bookings, name="bookings"),
        path("accounts/login/", login_view, name="login"),
        path("account/", account, name="account"),
        path("staff-list/", staff_list, name="staff_list"),
        path("register/", register_view, name="register"),
        path("logout/", logout_view, name="logout"),
        path("api/bookings/create/", create_booking, name="create_booking"),
        path("api/user/profile/", get_user_profile, name="get_user_profile"),
        path(
            "api/bookings/<int:booking_id>/status/",
            update_booking_status,
            name="update_booking_status",
        ),
        path("health/", health_check, name="health_check"),
        path("account/delete/", delete_account, name="delete_account"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
