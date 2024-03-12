from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from django.contrib.auth import login
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)  # Отправляем email после успешной регистрации
            return Response({"detail": "User registered successfully. Please check your email to verify."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




HOST_URL = 'http://127.0.0.1:8000/'


def send_verification_email(user, request):
    verification_code = str(user.email_verification.verification_code)
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'verification_code': verification_code}))

    subject = 'Verify Your Email'
    html_message = render_to_string('app/verification_email.html', {'verification_url': verification_url})
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]
    try:
        email = EmailMessage(subject, html_message, from_email, to_email)
        email.content_subtype = 'html'  # Это важно, чтобы письмо интерпретировалось как HTML
        email.send()
    except Exception as e:
        print(f'Error sending email: {e}')


def verify_email(request, verification_code):
    try:
        email_verification = EmailVerification.objects.get(verification_code=verification_code)
        if email_verification.verified:
            return HttpResponse('Email is already verified')
        email_verification.verified = True
        email_verification.user.is_active = True
        email_verification.user.save()
        email_verification.save()
        # Теперь можете сгенерировать и отправить токен аутентификации пользователю
        return HttpResponse('Email verified successfully')
    except EmailVerification.DoesNotExist:
        return HttpResponse('Invalid verification code', status=400)



@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    # Парсинг JSON-данных из тела запроса
    data = json.loads(request.body)

    # Создание формы с данными из запроса
    form = CustomUserCreationForm(data)

    # Проверка валидности формы
    if form.is_valid():
        # Создание но не сохранение нового пользователя
        user = form.save(commit=False)

        # Обработка и присвоение экземпляров Faculty и Specialty если они предоставлены
        faculty_id = data.get('faculty')
        specialty_id = data.get('specialty')

        if faculty_id:
            try:
                faculty = Faculty.objects.get(id=faculty_id)
                user.faculty = faculty
            except Faculty.DoesNotExist:
                return JsonResponse({"status": "error", "errors": {"faculty": ["Faculty not found."]}}, status=400)

        if specialty_id:
            try:
                specialty = Specialty.objects.get(id=specialty_id)
                user.specialty = specialty
            except Specialty.DoesNotExist:
                return JsonResponse({"status": "error", "errors": {"specialty": ["Specialty not found."]}}, status=400)

        # Сохранение пользователя после обработки всех полей
        user.save()

        # Не забудьте сохранить форму m2m данных если это необходимо
        form.save_m2m()

        return JsonResponse({"status": "success", "user_id": user.id}, status=201)
    else:
        # Возврат ошибок, если данные невалидны
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)



@csrf_exempt
@require_http_methods(["POST"])
def book_room(request, room_id):
    # Получаем текущего пользователя (предполагается, что пользователь авторизован)
    user = request.user

    # Получаем комнату, которую студент хочет забронировать
    room = Room.objects.get(id=room_id)

    # Проверяем, что пользователь активен и имеет роль "Student"
    if user.is_active and user.role.name == 'Student':
        # Проверяем, что у пользователя нет активного бронирования
        if not Booking.objects.filter(user=user, is_active=True).exists():
            # Создаем новое бронирование
            booking = Booking.objects.create(user=user, room=room, requiredDocs=True, verification_code_entry_field="YourVerificationCodeHere")

            # Уменьшаем количество доступных мест в комнате
            room.AvailableSeats -= 1
            room.ReservedSeats += 1
            room.save()

            # Помечаем пользователя как активного (забронировал место)
            user.is_active = True
            user.save()

            return render(request, 'success_booking.html', {'booking': booking})
        else:
            return render(request, 'already_booked.html')
    else:
        return render(request, 'unauthorized_booking.html')


class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
