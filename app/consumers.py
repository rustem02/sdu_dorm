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
