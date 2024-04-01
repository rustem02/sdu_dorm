# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# from .models import Seat
# from .serializers import SeatSerializer
# from channels.db import database_sync_to_async
#
# class AvailableSeatsConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#
#         seats = await self.get_available_seats()
#         await self.send(text_data=json.dumps({
#             'type': 'available_seats',
#             'message': seats
#         }))
#
#     async def disconnect(self, close_code):
#         pass
#
#     @database_sync_to_async
#     def get_available_seats(self):
#         seats = Seat.objects.filter(is_reserved=False)
#         serializer = SeatSerializer(seats, many=True)
#         return serializer.data





# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import AnonymousUser
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# import json
# from urllib.parse import parse_qsl
#
#
# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Получаем параметры строки запроса из self.scope['query_string'] и декодируем их
#         query_string = self.scope['query_string'].decode()
#         params = dict(parse_qsl(query_string))
#         token = params.get('token')
#
#         if token:
#             self.user = await self.get_user_from_token(token)
#             if self.user and self.user.is_authenticated:
#                 self.room_group_name = f'notifications_{self.user.id}'
#                 await self.channel_layer.group_add(
#                     self.room_group_name,
#                     self.channel_name
#                 )
#                 await self.accept()
#             else:
#                 self.user = AnonymousUser()
#                 await self.close()
#         else:
#             self.user = AnonymousUser()
#             await self.close()
#
#     async def disconnect(self, close_code):
#         if hasattr(self, 'room_group_name'):
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )
#
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         token = text_data_json.get('token')
#
#         if token:
#             self.user = await self.get_user_from_token(token)
#             if self.user is not None and self.user.is_authenticated:
#                 self.room_group_name = f'notifications_{self.user.id}'
#                 await self.channel_layer.group_add(
#                     self.room_group_name,
#                     self.channel_name
#                 )
#             else:
#                 await self.close()
#
#     async def notification_message(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))
#
#     @database_sync_to_async
#     def get_user_from_token(self, token_key):
#         try:
#             token = Token.objects.get(key=token_key)
#             return token.user
#         except Token.DoesNotExist:
#             return AnonymousUser()

