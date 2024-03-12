# serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid email/password.")
        if not user.is_active:
            raise serializers.ValidationError("User is inactive.")
        return user

# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['id', 'user', 'room', 'start_date', 'end_date']
#         read_only_fields = ('user',)  # Пользователь будет устанавливаться автоматически
#
#     def create(self, validated_data):
#         # Установка пользователя из контекста запроса
#         validated_data['user'] = self.context['request'].user
#         return super().create(validated_data)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['bookingID', 'user', 'room', 'requiredDocs', 'verification_code_entry_field', 'start_date', 'end_date', 'created_at', 'is_active']
        read_only_fields = ('user', 'created_at', 'bookingID')  # Защищаем некоторые поля от изменений

    def create(self, validated_data):
        # Добавляем пользователя из контекста запроса
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        """
        Валидация дат: начальная дата не может быть позже конечной.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must occur after start date")
        return data


class SubmissionDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDocuments
        fields = ['statement', 'photo_3x4', 'form_075', 'identity_card_copy']