from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm
from .models import User, Room, Booking
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
# from .forms import UserCreationForm


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'status': 'Registration successful!'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'status': 'GET request received for registration view'})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'status': 'Login successful!'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    elif request.method == 'GET':
        return JsonResponse({'status': 'GET request received for login view'})


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
