from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Faculty)
admin.site.register(User)
# admin.site.register(Role)
admin.site.register(Specialty)
admin.site.register(Room)
admin.site.register(SubmissionDocuments)
admin.site.register(Booking)
admin.site.register(Seat)
admin.site.register(News)
admin.site.register(Review)
admin.site.register(DefaultPayment)
admin.site.register(PasswordResetToken)