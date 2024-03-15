from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Faculty, Specialty
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.hashers import make_password



User = get_user_model()


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'id_number', 'faculty', 'specialty', 'gender']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Password does not match")

        return cleaned_data

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data["password"])

        if commit:
            user.save()
            # Сохранение связанных объектов после сохранения пользователя
            self.save_m2m()
        return user



class DocumentSubmissionForm(forms.ModelForm):
    class Meta:
        model = SubmissionDocuments
        fields = ['statement', 'photo_3x4', 'form_075', 'identity_card_copy']

