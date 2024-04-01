"""
ASGI config for sdu_dorm project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdu_dorm.settings')

application = get_asgi_application()


# import os
# import django
#
# # import sdu_dorm
# # from .wsgi import *
# # import sys
# # from channels.auth import AuthMiddlewareStack
# # from channels.routing import ProtocolTypeRouter, URLRouter
# # from channels.routing import get_default_application
# # from django.core.asgi import get_asgi_application
# # from django.urls import path
# # from sdu_dorm.routing import websocket_urlpatterns  # Импорт путей для WebSocket
# #
# # sys.path.append("/var/www/new-personality-server-2.0/personality")
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdu_dorm.settings')
# #
# # django.setup()
# # application = ProtocolTypeRouter({
# #     "http": get_asgi_application(),
# #     # Путь к вашим маршрутам WebSocket может выглядеть примерно так
# #     "websocket": AuthMiddlewareStack(
# #         URLRouter(
# #             sdu_dorm.routing.websocket_urlpatterns
# #         )
# #     ),
# # })
#
# # asgi.py
# import os
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from . import routing
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdu_dorm.settings')
#
# application = ProtocolTypeRouter({
#   "http": get_asgi_application(),
#   "websocket": AuthMiddlewareStack(
#         URLRouter(
#             routing.websocket_urlpatterns
#         )
#     ),
# })
