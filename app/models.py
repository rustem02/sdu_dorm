from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import uuid

class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))

        return self.create_user(email, password, **extra_fields)

# Пользовательская модель
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=20, null=True, blank=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, related_name='faculty_users')
    specialty = models.ForeignKey('Specialty', on_delete=models.SET_NULL, null=True, related_name='specialty_users')
    gender = models.CharField(max_length=10, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_doc_submitted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_dorm = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        unique_together = [['id', 'email']]

    def __str__(self):
        return self.email


class SubmissionDocuments(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submission_documents')
    statement = models.FileField(upload_to='documents/statement/', null=True, blank=True)
    photo_3x4 = models.FileField(upload_to='documents/photo_3x4/', null=True, blank=True)
    form_075 = models.FileField(upload_to='documents/form_075/', null=True, blank=True)
    identity_card_copy = models.FileField(upload_to='documents/identity_card/', null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name='Verified Status')
    admin_comments = models.TextField(blank=True, null=True, verbose_name='Admin Comments')


    def __str__(self):
        return f"Documents for {self.user.email}"

# class SubmissionDocuments(models.Model):
#     DOCUMENT_STATUS_CHOICES = (
#         ('not_submitted', 'Not Submitted'),
#         ('submitted', 'Submitted'),
#         ('verified', 'Verified'),
#     )
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     statement_status = models.CharField(max_length=12, choices=DOCUMENT_STATUS_CHOICES, default='not_submitted')
#     photo_status = models.CharField(max_length=12, choices=DOCUMENT_STATUS_CHOICES, default='not_submitted')
#     form_075_status = models.CharField(max_length=12, choices=DOCUMENT_STATUS_CHOICES, default='not_submitted')
#     # Повторите для других документов


class Room(models.Model):
    BLOCK_CHOICES = (
        ('A', 'Block A'),
        ('B', 'Block B'),
        ('C', 'Block C'),
        ('D', 'Block D'),
    )

    block = models.CharField(max_length=1, choices=BLOCK_CHOICES)
    room_number = models.IntegerField()  # Изменил RoomID на room_number для ясности
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    reserved_seats = models.IntegerField()

    def __str__(self):
        return f'{self.block} - Room {self.room_number}'


class Seat(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.IntegerField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f'Seat {self.seat_number} in {self.room}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')

    SEMESTER_CHOICES = (
        (1, "1 semester"),
        (2, "2 semesters"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
                                      # default=timezone.now
                                      )
    is_active = models.BooleanField(default=True)
    semester_duration = models.IntegerField(choices=SEMESTER_CHOICES, default=1, verbose_name='Duration in Semesters')


    def __str__(self):
        return f'Booking by {self.user.email} for {self.semester_duration} semester(s)'

    # def release_seats(self):
    #     for booking in Booking.objects.filter(end_date__lt=timezone.now(), is_active=True):
    #         booking.seat.is_reserved = False
    #         booking.seat.save()
    #         booking.is_active = False
    #         booking.save()


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    sum = models.CharField(max_length=16)
    # created_at = models.DateTimeField(
    #     auto_now_add=True,
    #     # default=timezone.now
    # )
    card_number = models.CharField(max_length=16)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    cvv = models.IntegerField()
    email = models.EmailField()
    telephone_number = models.CharField(max_length=15)

    def __str__(self):
        return f'Payment for Booking ID {self.booking.id} by {self.user.email}'

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    sum = models.CharField(max_length=16)
    created_at = models.DateTimeField(
        auto_now_add=True,
        # default=timezone.now
    )

    def __str__(self):
        return f'Payment for Booking ID {self.booking.id} by {self.user.email}'

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to='news/file/', null=True, blank=True)
    datePublished = models.DateField(
        auto_now_add=True,
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')

    def save(self, *args, **kwargs):
        if self.author.is_staff:
            super().save(*args, **kwargs)
        else:
            raise ValueError("Only Admins can create News")

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    datePublished = models.DateField(auto_now_add=True,)

    def __str__(self):
        return f'Review by {self.user.email}'


User = get_user_model()

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False)
    verified = models.BooleanField(default=False)