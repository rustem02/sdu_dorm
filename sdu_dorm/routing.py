# from .wsgi import *
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path, re_path
# from app.consumers import AvailableSeatsConsumer  # Импортируйте вашего потребителя
#
# websocket_urlpatterns = [
#     re_path(r'ws/available-seats/$', AvailableSeatsConsumer.as_asgi()),
# ]
#
# application = ProtocolTypeRouter({
#     'websocket': URLRouter(websocket_urlpatterns),
# })
