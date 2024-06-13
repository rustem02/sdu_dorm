# serializers.py
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import password_validation


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






class BookingSerializer(serializers.ModelSerializer):
    block = serializers.CharField(write_only=True)
    room_number = serializers.CharField(write_only=True)
    seat_number = serializers.IntegerField(write_only=True)
    semester_duration = serializers.IntegerField()

    class Meta:
        model = Booking
        fields = ['id','user', 'block', 'room_number', 'seat_number', 'semester_duration']
        read_only_fields = ('user', 'id')

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

class GetAllSpecialities(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = '__all__'

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
            booking = obj.bookings.filter(is_active=True).first()  # активное бронирование может быть только одно
            if booking:
                return booking.user.email  # Или любая другая информация о пользователе
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = self.context['request'].user
        if (user.gender == 'Male' and instance.room.block not in ['C', 'D']) or \
           (user.gender == 'Female' and instance.room.block not in ['A', 'B']):
            return None  # Вместо пустого объекта лучше возвращать None для фильтрации во view, надо допилить;)
        return representation


class UserSerializer(serializers.ModelSerializer):
    faculty_name = serializers.SerializerMethodField()
    specialty_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'id_number', 'faculty_name', 'specialty_name']

    def get_faculty_name(self, obj):
        return obj.faculty.name if obj.faculty else None

    def get_specialty_name(self, obj):
        return obj.specialty.name if obj.specialty else None


class RoomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'block', 'room_number']

class GetBookingSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    # room_detail = RoomDetailSerializer(source='room', read_only=True)
    seat_detail = SeatSerializer(source='seat', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user_data', 'seat_detail', 'semester_duration']
        read_only_fields = ('id',)



# добавил user_data для запроса гет документс
class GetSubmissionDocumentSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionDocuments
        fields = ['statement', 'photo_3x4', 'form_075', 'identity_card_copy', 'is_verified', 'admin_comments',
                  'user_data']

    def get_user_data(self, obj):
        user = obj.user
        user_serializer = UserSerializer(user)
        return user_serializer.data


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
            bookings = Booking.objects.filter(user=obj, is_active=True)
            if bookings.exists():
                return BookingSerializer(bookings, many=True).data
            else:
                return "No bookings made."
        else:
            return "Access restricted."


class UserProfileSerializer(serializers.ModelSerializer):
    submission_documents = serializers.SerializerMethodField()
    bookings = serializers.SerializerMethodField()
    faculty_name = serializers.SerializerMethodField()
    specialty_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'id_number', 'faculty_name', 'specialty_name', 'gender', 'submission_documents', 'bookings', 'is_dorm', 'is_doc_submitted']

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
        bookings = Booking.objects.filter(user=obj)
        if bookings.exists():
            return GetBookingSerializer(bookings, many=True, context={'request': self.context['request']}).data
        else:
            return "No bookings made."

    def get_faculty_name(self, obj):
        return obj.faculty.name if obj.faculty else None

    def get_specialty_name(self, obj):
        return obj.specialty.name if obj.specialty else None



class SubmissionDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDocuments
        fields = ['statement', 'photo_3x4', 'form_075', 'identity_card_copy']
        extra_kwargs = {'statement': {'required': True}, 'photo_3x4': {'required': True},
                        'form_075': {'required': True}, 'identity_card_copy': {'required': True}
                        }

    def update(self, instance, validated_data):
        instance.statement = validated_data.get('statement', instance.statement)
        instance.photo_3x4 = validated_data.get('photo_3x4', instance.photo_3x4)
        instance.form_075 = validated_data.get('form_075', instance.form_075)
        instance.identity_card_copy = validated_data.get('identity_card_copy', instance.identity_card_copy)
        instance.save()

        # Проверка наличия всех документов и обновление статуса в модели User
        user = instance.user
        # if instance.statement and instance.photo_3x4 and instance.form_075 and instance.identity_card_copy:
        user.is_doc_submitted = True
        user.save()

        return instance


class DocumentDeletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDocuments
        fields = ['statement', 'photo_3x4', 'form_075', 'identity_card_copy']

    def update(self, instance, validated_data):
        # обновляем только те поля которые удаляемz
        for field_name in self.fields:
            if validated_data.get(field_name) is None:
                setattr(instance, field_name, None)
        instance.save()
        return instance


class SubmissionDocumentsSerializerForAdmin(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = SubmissionDocuments
        fields = ['user','statement', 'photo_3x4', 'form_075', 'identity_card_copy', 'is_verified', 'admin_comments']
        extra_kwargs = {'statement': {'required': True}, 'photo_3x4': {'required': True},
                        'form_075': {'required': True}, 'identity_card_copy': {'required': True},
                        'is_verified': {'required': False}, 'admin_comments': {'required': False}}

    def update(self, instance, validated_data):
        instance.statement = validated_data.get('statement', instance.statement)
        instance.photo_3x4 = validated_data.get('photo_3x4', instance.photo_3x4)
        instance.form_075 = validated_data.get('form_075', instance.form_075)
        instance.identity_card_copy = validated_data.get('identity_card_copy', instance.identity_card_copy)
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.admin_comments = validated_data.get('admin_comments', instance.admin_comments)
        instance.save()

        # Проверка наличия всех документов и обновление статуса в модели User
        user = instance.user
        # if instance.statement and instance.photo_3x4 and instance.form_075 and instance.identity_card_copy:
        #     user.is_doc_submitted = True
        user.save()

        return instance




# Получить документы для админа
class GetAllSubmissionDocumentsSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionDocuments
        fields = ['statement', 'photo_3x4', 'form_075', 'identity_card_copy', 'is_verified', 'admin_comments', 'user_data']

    def get_user_data(self, obj):
        user = obj.user
        user_serializer = UserSerializer(user)
        return user_serializer.data



channel_layer = get_channel_layer()
def send_notification(user_id, message):
    group_name = f'notifications_{user_id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'notification_message',
            'message': message
        }
    )


class DocumentVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionDocuments
        fields = ['is_verified', 'admin_comments']

    def update(self, instance, validated_data):
        # Обновляем экземпляр SubmissionDocuments с новыми данными
        instance.is_verified = validated_data.get('is_verified', instance.is_verified)
        instance.admin_comments = validated_data.get('admin_comments', instance.admin_comments)
        instance.save()

        if instance.is_verified:
            send_mail(
                'Ваши документы проверены',
                'Ваши документы были успешно проверены. Перейдите на сайт, чтобы приступить к бронированию. ' +
                'Ссылка на сайт: https://front-deploy-beta.vercel.app/',
                settings.DEFAULT_FROM_EMAIL,
                [instance.user.email],
                fail_silently=False,
            )

        return instance


# Новости

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'file', 'datePublished', 'author']
        read_only_fields = ('author', 'datePublished')  # Author will be set in the view, and datePublished is auto-set



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultPayment
        fields = ['amount', 'booking']

    def create(self, validated_data):
        user = self.context['request'].user  # Получаем пользователя
        validated_data['user'] = user  # Добавляем пользователя для объекта
        payment = DefaultPayment.objects.create(**validated_data)

        user.is_dorm = True
        user.save()
        return payment

    def validate_booking(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError("This booking does not belong to the current user.")
        if user.is_dorm:
            raise serializers.ValidationError("This booking has already been paid for.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # User = settings.AUTH_USER_MODEL
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email не найден.")
        return value

    def save(self):
        # User = settings.AUTH_USER_MODEL
        user = User.objects.get(email=self.validated_data['email'])
        token = PasswordResetToken.objects.create(user=user).token
        reset_url = f"http://13.49.18.134/password-reset/{token}/"
        send_mail(
            'Сброс пароля',
            f'Перейдите по ссылке для сброса пароля: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [self.validated_data['email']],
            fail_silently=False,
        )

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        try:
            token = PasswordResetToken.objects.get(token=attrs.get('token'))
            if token.created_at < timezone.now() - timedelta(hours=24):
                raise serializers.ValidationError("Токен сброса пароля истек.")
            return {'user': token.user, 'password': attrs.get('password')}
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Неверный токен сброса пароля")

    def save(self, **kwargs):
        user = self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save()
        # Удалить использованный токен
        PasswordResetToken.objects.filter(user=user).delete()



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Неверный текущий пароль.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"confirm_new_password": "Новые пароли не совпадают."})
        password_validation.validate_password(data['new_password'], self.context['request'].user)
        return data




class ReviewSerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['id', 'user_data', 'comment', 'datePublished', 'rate', 'likes', 'reply_to']

    def get_user_data(self, obj):
        user = obj.user
        user_serializer = UserSerializer(user)
        return user_serializer.data

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['comment', 'rate', 'reply_to']

    def create(self, validated_data):
        # надо добавить дополнительную логику отправку уведомлений!!
        return Review.objects.create(**validated_data, user=self.context['request'].user)


# class UserUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'birth_date', 'faculty', 'specialty']
#
#     def update(self, instance, validated_data):
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.birth_date = validated_data.get('birth_date', instance.birth_date)
#
#         faculty_id = validated_data.get('faculty')
#         if faculty_id:
#             instance.faculty = Faculty.objects.filter(id=faculty_id).first()
#
#         specialty_id = validated_data.get('specialty')
#         if specialty_id:
#             instance.specialty = Specialty.objects.filter(id=specialty_id).first()
#
#         instance.save()
#         return instance