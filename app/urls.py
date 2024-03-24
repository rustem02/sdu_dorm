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
    # Auth
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('verify-email/<uuid:verification_code>/', verify_email, name='verify_email'),

    # Submission documents
    path('documents/upload/', SubmissionDocumentsView.as_view(), name='documents-upload'),
    path('documents/get/', SubmissionDocumentsListView.as_view(), name='documents-list'),
    # Нужны права администратора
    path('user-documents/<int:pk>/', UserDocumentsByIDView.as_view(), name='user-documents-by-id'),
    path('api/documents/verify/<int:pk>/', DocumentVerificationView.as_view(), name='document-verification'),


    # Booking
    path('api/bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('api/get-bookings/', BookingListView.as_view(), name='booking-list'),
    path('cancel-booking/<int:booking_id>/', CancelBookingView.as_view(), name='cancel-booking'),

    path('api/available-seats/', AvailableSeatsListView.as_view(), name='available-seats'),
    # path('book_room/<int:room_id>/', book_room, name='book_room'),


    path('api/users/', UserListView.as_view(), name='user-list'),
    # по эмайлу пользователя
    path('user-details/', UserDetailView.as_view(), name='user-details'),

    # path('api/rooms/', views.RoomListView.as_view(), name='room-list'),
    #
    # path('api/rooms/<int:block_id>/<int:room_id>/<int:seat_id>/', views.RoomDetailView.as_view(), name='room-detail'),
    #
    # path('api/bookings/', views.BookingListView.as_view(), name='booking-list'),
    #
    # path('api/bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    #
    # path('api/payments/', views.PaymentListView.as_view(), name='payment-list'),
    #
    # path('api/payments/<int:user_id>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    #
    # path('api/news/', views.NewsListView.as_view(), name='news-list'),
    #
    # path('api/news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    #
    # path('api/reviews/', views.ReviewListView.as_view(), name='review-list'),
    #
    # path('api/reviews/<int:user_id>/', views.ReviewDetailView.as_view(), name='review-detail'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
