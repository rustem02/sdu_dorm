from django.contrib import admin
from django.urls import path
from .views import *
from django.conf.urls.static import static


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


    # Booking
    path('api/bookings/', BookingCreateAPIView.as_view(), name='booking-create'),
    path('api/get-bookings/', BookingListView.as_view(), name='booking-list'),
    path('cancel-booking/<int:booking_id>/', CancelBookingView.as_view(), name='cancel-booking'),

    path('api/available-seats/', AvailableSeatsListView.as_view(), name='available-seats'),
    # path('book_room/<int:room_id>/', book_room, name='book_room'),


    path('api/users/', UserListView.as_view(), name='user-list'),
    path('user-details/<int:user_id>/', UserDetailView.as_view(), name='user-details'),

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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
