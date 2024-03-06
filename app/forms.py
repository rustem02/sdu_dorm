from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Faculty, Specialty
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # Используем get_user_model вместо прямого указания модели
        # Укажите все поля, которые вы хотите включить в форму регистрации, кроме 'password1' и 'password2', которые уже включены по умолчанию.
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'birth_date', 'id_number', 'faculty', 'specialty', 'gender',)
    # Определения полей и Meta класс...

    def save(self, commit=True):
        user = super().save(commit=False)
        faculty_id = self.cleaned_data.get('faculty')
        specialty_id = self.cleaned_data.get('specialty')

        if faculty_id:
            user.faculty_id = faculty_id  # Присваиваем ID напрямую

        if specialty_id:
            user.specialty_id = specialty_id  # Аналогично для специальности

        if commit:
            user.save()
        return user

