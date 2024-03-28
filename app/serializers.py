# serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from django.db import transaction

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
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            birth_date=validated_data['birth_date'],
            id_number=validated_data['id_number'],
            faculty=validated_data['faculty'],
            specialty=validated_data['specialty'],
            gender=validated_data['gender'],
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
            raise serializers.ValidationError("User is inactive. Please confirm email")
        return user




# class BookingSerializer(serializers.ModelSerializer):
#     room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
#     seat = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())
#
#     class Meta:
#         model = Booking
#         fields = ['user', 'room', 'seat', 'semester_duration']
#         read_only_fields = ('user',)
#
#     def validate(self, data):
#         """
#         Проверяем, что место принадлежит выбранной комнате.
#         """
#         room = data.get('room')
#         seat = data.get('seat')
#         user = self.context['request'].user
#         if seat.room != room:
#             raise serializers.ValidationError("The seat does not belong to the selected room.")
#         if seat.is_reserved:
#             raise serializers.ValidationError("This seat is already reserved.")
#         # if data['seat'].is_reserved:
#         #     raise serializers.ValidationError("This seat is already reserved.")
#         if Booking.objects.filter(user=user, is_active=True).exists():
#             raise serializers.ValidationError("You have already booked a seat.")
#         if not user.submission_documents.is_verified:
#             raise serializers.ValidationError("Your documents have not been verified yet.")
#         # return data
#         return data
#
#     def create(self, validated_data):
#         with transaction.atomic():
#             # Remove the 'user' key from validated_data if it exists to avoid conflicts
#             validated_data.pop('user', None)
#
#             # Explicitly set the user to the request user from the context
#             user = self.context['request'].user
#
#             # Set the seat as reserved
#             seat = validated_data['seat']
#             if not seat.is_reserved:
#                 seat.is_reserved = True
#                 seat.save()
#             else:
#                 raise serializers.ValidationError({"seat": "This seat is already reserved."})
#
#             # Check documents and create the booking
#             if not user.is_doc_submitted or not user.submission_documents.is_verified:
#                 raise serializers.ValidationError("Your documents are not verified or submitted.")
#
#             booking = Booking.objects.create(**validated_data, user=user)
#
#         return booking


class BookingSerializer(serializers.ModelSerializer):
    block = serializers.CharField(write_only=True)
    room_number = serializers.CharField(write_only=True)
    seat_number = serializers.IntegerField(write_only=True)
    semester_duration = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ['user', 'block', 'room_number', 'seat_number', 'semester_duration']
        read_only_fields = ('user',)

    def validate(self, data):
        user = self.context['request'].user

        # Дополнительные проверки
        if not user.is_doc_submitted:
            raise serializers.ValidationError("You need to submit your documents before making a booking.")

        if not user.submission_documents.is_verified:
            raise serializers.ValidationError("Your documents have not been verified yet.")

        block = data.get('block')
        room_number = data.get('room_number')
        seat_number = data.get('seat_number')

        if Booking.objects.filter(user=user, is_active=True).exists():
            raise serializers.ValidationError(
                "You already have an active booking. Please cancel it before making a new one.")

        room = Room.objects.filter(block=block, room_number=room_number).first()
        if not room:
            raise serializers.ValidationError("Room not found.")

        seat = Seat.objects.filter(room=room, seat_number=seat_number).first()
        if not seat:
            raise serializers.ValidationError("Seat not found in the specified room.")

        if seat.is_reserved:
            raise serializers.ValidationError("This seat is already reserved.")

        data['room'] = room
        data['seat'] = seat
        return data

    def create(self, validated_data):
        validated_data.pop('block', None)
        validated_data.pop('room_number', None)
        validated_data.pop('seat_number', None)

        user = self.context['request'].user

        seat = validated_data['seat']
        seat.is_reserved = True
        seat.save()

        booking = Booking.objects.create(**validated_data, user=user)
        return booking


# class SeatSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Seat
#         fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    room_number = serializers.SerializerMethodField()
    block = serializers.SerializerMethodField()
    reserved_by = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'block', 'room_number', 'is_reserved', 'reserved_by']

    def get_room_number(self, obj):
        return obj.room.room_number

    def get_block(self, obj):
        return obj.room.block

    def get_reserved_by(self, obj):
        if obj.is_reserved:
            booking = obj.bookings.filter(is_active=True).first()  # Предполагаем, что активное бронирование может быть только одно
            if booking:
                return booking.user.email  # Или любая другая информация о пользователе, которая вам нужна
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context['request'].user
        if (user.gender == 'Male' and instance.room.block not in ['C', 'D']) or \
           (user.gender == 'Female' and instance.room.block not in ['A', 'B']):
            return None  # Вместо пустого объекта лучше возвращать None для фильтрации во view
        return representation

class GetSubmissionDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDocuments
        fields = '__all__'


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'id_number', 'faculty', 'specialty', 'gender', 'submission_documents', 'bookings', 'is_dorm', 'is_doc_submitted']


class UserDetailsSerializer(serializers.ModelSerializer):
    submission_documents = serializers.SerializerMethodField()
    bookings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'id_number', 'faculty', 'specialty', 'gender', 'submission_documents', 'bookings', 'is_dorm', 'is_doc_submitted']

    def get_submission_documents(self, obj):
        # Получаем пользователя, который делает запрос
        request_user = self.context['request'].user
        # Проверяем, является ли пользователь администратором
        if request_user.is_staff:
            try:
                documents = SubmissionDocuments.objects.get(user=obj)
                return SubmissionDocumentsSerializer(documents).data
            except SubmissionDocuments.DoesNotExist:
                return "No documents submitted."
        else:
            # Ограничиваем доступ, если пользователь не является администратором
            return "Access restricted."

    def get_bookings(self, obj):
        request_user = self.context['request'].user
        # Аналогичная проверка для бронирований
        if request_user.is_staff:
            bookings = Booking.objects.filter(user=obj)
            if bookings.exists():
                return BookingSerializer(bookings, many=True).data
            else:
                return "No bookings made."
        else:
            return "Access restricted."


class UserProfileSerializer(serializers.ModelSerializer):
    submission_documents = serializers.SerializerMethodField()
    bookings = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'id_number', 'faculty', 'specialty', 'gender', 'submission_documents', 'bookings', 'is_dorm', 'is_doc_submitted']

    def get_submission_documents(self, obj):
        # Получаем пользователя, который делает запрос
        request_user = self.context['request'].user
        # Проверяем, является ли пользователь администратором

        try:
            documents = SubmissionDocuments.objects.get(user=obj)
            return SubmissionDocumentsSerializer(documents).data
        except SubmissionDocuments.DoesNotExist:
            return "No documents submitted."


    def get_bookings(self, obj):
        request_user = self.context['request'].user
        # Аналогичная проверка для бронирований

        bookings = Booking.objects.filter(user=obj)
        if bookings.exists():
            return BookingSerializer(bookings, many=True).data
        else:
            return "No bookings made."



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


class DocumentVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDocuments
        fields = ['is_verified', 'admin_comments']


# Новости

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'file', 'datePublished', 'author']
        read_only_fields = ('author', 'datePublished')  # Author will be set in the view, and datePublished is auto-set


