from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # Добавьте дополнительные поля, если необходимо
    # student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=20, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='faculty_users')
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, related_name='specialty_users')
    gender = models.CharField(max_length=10, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_dorm = models.BooleanField(default=False)

    class Meta:
        # Добавляем уникальный ограничивающий индекс для полей, которые есть и в auth.User
        unique_together = ['id', 'username']

    # Убеждаемся, что связанные имена не пересекаются с auth.User
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)

class SubmissionDocuments(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    statement = models.BooleanField()
    photo_3x4 = models.BooleanField()
    form_075 = models.BooleanField()
    identity_card_copy = models.BooleanField()
    power_of_attorney = models.BooleanField()
    address_certificate = models.BooleanField()
    university_admission_form = models.BooleanField()

class Room(models.Model):
    BlockID = models.IntegerField()
    RoomID = models.IntegerField()
    SeatID = models.IntegerField()
    TotalSeats = models.IntegerField()
    AvailableSeats = models.IntegerField()
    ReservedSeats = models.IntegerField(primary_key=True)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    bookingID = models.AutoField(primary_key=True)
    requiredDocs = models.BooleanField()
    verification_code_entry_field = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)


class Payment(models.Model):
    card_number = models.CharField(max_length=16)
    expiration_month = models.IntegerField()
    expiration_year = models.IntegerField()
    cvv = models.IntegerField()
    email = models.EmailField(max_length=255)
    telephone_number = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class News(models.Model):
    NewsID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Content = models.TextField()
    DatePublished = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.author.role.name == 'Admin':
            super().save(*args, **kwargs)
        else:
            raise ValueError("Only Admins can create News")

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    datePublished = models.DateField()
