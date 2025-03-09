from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Language


class UserRegisterForm(UserCreationForm):
    languages = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select languages you speak (only required for staff)",
    )

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
            "languages",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show languages field for staff registration
        self.fields["languages"].widget.attrs["class"] = "staff-only-field"

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data.get("picture"):
                user.picture = self.cleaned_data.get("picture")
                user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        languages = cleaned_data.get("languages")

        if user_type == "staff" and not languages:
            self.add_error(
                "languages", "Staff members must select at least one language"
            )

        return cleaned_data
