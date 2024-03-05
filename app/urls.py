from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('book_room/<int:room_id>/', book_room, name='book_room'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    # path('api/users/', views.UserListView.as_view(), name='user-list'),
    #
    # path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    #
    # path('api/documents/', views.SubmissionDocumentsView.as_view(), name='submission-documents'),
    #
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

]
