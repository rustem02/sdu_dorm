from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import *
from rest_framework import status, permissions
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated,  BasePermission
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import unquote

class HomePage(ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return News.objects.all()

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_verification_email(user, request)  # Отправляем email после успешной регистрации
            return Response({"detail": "User registered successfully. Please check your email to verify."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutAPIView(APIView):
#     def post(self, request):
#         logout(request)
#         return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

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
        # Генерация токена
        return HttpResponse('Email verified successfully')
    except EmailVerification.DoesNotExist:
        return HttpResponse('Invalid verification code', status=400)


class IsOwnerOrAdmin(BasePermission):
    """
    Разрешение, которое позволяет доступ только владельцу ресурса или администратору.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff


class BookingCreateAPIView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        # Проверяем, подтверждены ли документы пользователя
        if not user.submission_documents.is_verified:
            raise Response({"error": "Your documents have not been verified yet."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()


class BookingListView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        метод для фильтрованных брони, чтобы пользователь видел только свои бронирования.
        """
        user = self.request.user
        return Booking.objects.filter( is_active=True, user=user,)


class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id, user=request.user)

        # Проверяем, активно ли бронирование
        if not booking.is_active:
            return Response({"error": "This booking is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        # Отменяем бронирование
        booking.is_active = False
        booking.save()

        # Делаем место снова доступным, если необходимо
        seat = booking.seat
        seat.is_reserved = False
        seat.save()

        return Response({"success": "Booking has been cancelled."}, status=status.HTTP_200_OK)



class AvailableSeatsListView(ListAPIView):
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает список свободных мест.
        """
        return Seat.objects.filter(is_reserved=False)


class UserListView(ListAPIView):
    serializer_class = GetUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает список пользователей.
        """
        return User.objects.filter(is_active=True)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email parameter is required."}, status=400)

        user = get_object_or_404(User, email=email)
        serializer = UserDetailsSerializer(user, context={'request': request})
        return Response(serializer.data)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user

        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)



class SubmissionDocumentsListView(ListAPIView):
    serializer_class = GetSubmissionDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает список документов текущего пользователя.
        """
        user = self.request.user
        return SubmissionDocuments.objects.filter(user=user)




class UserDocumentsByIDView(RetrieveAPIView):
    queryset = SubmissionDocuments.objects.all()
    serializer_class = SubmissionDocumentsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        """
        Возвращает документы для указанного ID пользователя.
        """
        user_id = self.kwargs['pk']
        document = get_object_or_404(SubmissionDocuments, user__id=user_id)
        self.check_object_permissions(self.request, document)
        return document



class DocumentVerificationView(generics.UpdateAPIView):
    queryset = SubmissionDocuments.objects.all()
    serializer_class = DocumentVerificationSerializer
    permission_classes = [IsOwnerOrAdmin]  # Позволяет доступ только администраторам

    def get_object(self):
        # Вы можете использовать 'pk' из URL для получения конкретного экземпляра SubmissionDocuments
        return get_object_or_404(SubmissionDocuments, pk=self.kwargs['pk'])

class SubmissionDocumentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            submission_documents = SubmissionDocuments.objects.get(user=user)
        except SubmissionDocuments.DoesNotExist:
            submission_documents = None

        if submission_documents:
            serializer = SubmissionDocumentsSerializer(submission_documents, data=request.data)
        else:
            serializer = SubmissionDocumentsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow admins to edit it.
    Assumes the model instance has an `is_staff` attribute.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to staff users.
        return request.user and request.user.is_staff

class NewsListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUserOrReadOnly, permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the author to the current user
        serializer.save(author=self.request.user)

class NewsUpdateView(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]  # Only allow access to admin users

    def perform_update(self, serializer):
        serializer.save()  # Additional actions can be performed here