from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "user_type",
            "street",
            "street_number",
            "apartment",
            "city",
            "state",
            "zip_code",
            "country",
            "picture",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data.get('picture'):
                user.picture = self.cleaned_data.get('picture')
                user.save()
        return user
