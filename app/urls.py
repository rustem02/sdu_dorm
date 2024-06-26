from django.contrib import admin
from django.urls import path, re_path
from .views import *
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# надо доработать
schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="API description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Home
    path('', HomePage.as_view(), name='home'),
    # Auth
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('verify-email/<uuid:verification_code>/', verify_email, name='verify_email'),

    # Reset password
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/<uuid:token>/', PasswordResetView.as_view(), name='password-reset'),

    # Submission documents
    path('api/documents/upload/', SubmissionDocumentsView.as_view(), name='documents-upload'),
    path('api/documents/update/', UpdateSubmissionDocumentsView.as_view(), name='documents-upload'),
    path('api/documents/get/', SubmissionDocumentsListView.as_view(), name='documents-list'),
    # path('api/documents/delete/', DeleteDocumentFileView.as_view(), name='partial-document-deletion'),
    path('api/delete-document/<str:file_field>/', DeleteDocumentFileView.as_view(), name='delete-document-file'),

                  # получить все документы, админ
    path('api/documents/', GetAllSubmissionDocumentsListView.as_view(), name='submission-documents-list'),
    # Нужны права администратора
    path('api/user-documents/<int:pk>/', UserDocumentsByIDView.as_view(), name='user-documents-by-id'),
    # получить документ по емайлу, админ
    path('api/user-documents/', UserDocumentsByEmailView.as_view(), name='user-documents-by-email'),
    path('api/documents/verify/', DocumentVerificationView.as_view(), name='document-verification'),


    # Booking
    path('api/bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('api/get-bookings/', BookingListView.as_view(), name='booking-list'),
    path('api/cancel-booking/', CancelBookingView.as_view(), name='cancel-booking'),

    path('api/available-seats/', AvailableSeatsListView.as_view(), name='available-seats'),
    path('api/rooms/', AvailableSeatsAPIView.as_view(), name='available-rooms'),



    # Users
    path('api/users/', UserListView.as_view(), name='user-list'),
    # по эмайлу пользователя
    path('api/user-details/', UserDetailView.as_view(), name='user-details'),

    # news
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/', NewsUpdateView.as_view(), name='news-update'),
    path('news-detail/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),

    # Profile
    path('api/profile/', ProfileView.as_view(), name='user-profile'),


    # Payment
    path('api/payment/', PaymentAPIView.as_view(), name='payment'),
    path('api/payment/success/', PaymentSuccessAPIView.as_view(), name='payment-success'),
    path('api/payment/fail/', PaymentFailAPIView.as_view(), name='payment-fail'),
    path('api/payment/receipt/', PaymentReceiptAPIView.as_view(), name='payment-receipt'),
    path('api/payment/download-receipt/', DownloadReceiptAPIView.as_view(), name='download-receipt'),

    # Specialities
    path('api/specialities/', GetAllSpecialitiesView.as_view(), name='specialities'),

    # Change pass
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),

    # Review - отзыв
    path('api/review/', ReviewListView.as_view(), name='review-list'),
    # для swagger, не нужен
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
