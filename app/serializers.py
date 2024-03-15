# serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'birth_date', 'id_number', 'faculty', 'specialty', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False,  # Пользователь не активен до верификации email
            # Можно добавить остальные поля
        )
        EmailVerification.objects.create(user=user)  # Создание объекта EmailVerification
        return user

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


# Надо доделать!
# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = ['user', 'room', 'start_date', 'end_date', 'created_at']
#         read_only_fields = ('user', 'created_at')  # Защищаем некоторые поля от изменений
#
#     def create(self, validated_data):
#         # Добавляем пользователя из контекста запроса
#         validated_data['user'] = self.context['request'].user
#         docs = self.context['request'].user.is_doc_submitted
#         if docs == True:
#             return super().create(validated_data)
#         else:
#             raise serializers.ValidationError("You need to submit documents")
#
#     def validate(self, data):
#         """
#         Валидация дат: начальная дата не может быть позже конечной.
#         """
#         if data['start_date'] > data['end_date']:
#             raise serializers.ValidationError("End date must occur after start date")
#         return data

class BookingSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    seat = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())

    class Meta:
        model = Booking
        fields = ['user', 'room', 'seat', 'start_date', 'end_date']
        read_only_fields = ('user',)

    def validate(self, data):
        """
        Проверяем, что место принадлежит выбранной комнате.
        """
        room = data.get('room')
        seat = data.get('seat')
        if seat.room != room:
            raise serializers.ValidationError("The seat does not belong to the selected room.")
        if seat.is_reserved:
            raise serializers.ValidationError("This seat is already reserved.")
        return data

    def create(self, validated_data):
        # Устанавливаем место как зарезервированное
        seat = validated_data['seat']
        seat.is_reserved = True
        seat.save()

        # Проверка документов пользователя
        user = self.context['request'].user
        if not user.is_doc_submitted:
            raise serializers.ValidationError("You need to submit documents before making a booking.")

        booking = Booking.objects.create(**validated_data, user=user)
        return booking



class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'



class GetSubmissionDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDocuments
        fields = '__all__'



class SubmissionDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDocuments
        fields = ['statement', 'photo_3x4', 'form_075', 'identity_card_copy']
        extra_kwargs = {'statement': {'required': False}, 'photo_3x4': {'required': False},
                        'form_075': {'required': False}, 'identity_card_copy': {'required': False}}

    def update(self, instance, validated_data):
        instance.statement = validated_data.get('statement', instance.statement)
        instance.photo_3x4 = validated_data.get('photo_3x4', instance.photo_3x4)
        instance.form_075 = validated_data.get('form_075', instance.form_075)
        instance.identity_card_copy = validated_data.get('identity_card_copy', instance.identity_card_copy)
        instance.save()

        # Проверка наличия всех документов и обновление статуса в модели User
        user = instance.user
        if instance.statement and instance.photo_3x4 and instance.form_075 and instance.identity_card_copy:
            user.is_doc_submitted = True
            user.save()

        return instance
