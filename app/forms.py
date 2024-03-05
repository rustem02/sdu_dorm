from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


# надо доделать
class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(required=False)
    id_number = forms.CharField(max_length=20, required=False)
    faculty = forms.IntegerField(required=False)
    specialty = forms.IntegerField(required=False)
    gender = forms.CharField(max_length=10, required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'birth_date', 'id_number', 'faculty', 'specialty', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None