from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        # "user" is not here: the view sets it, so nobody can pick another user.
        fields = [
            "company",
            "role",
            "job_url",
            "location",
            "salary",
            "status",
            "date_applied",
            "follow_up_date",
            "notes",
        ]
        widgets = {
            "date_applied": forms.DateInput(attrs={"type": "date"}),
            "follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to every field.
        for name, field in self.fields.items():
            css = "form-select" if name == "status" else "form-control"
            field.widget.attrs["class"] = css


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
