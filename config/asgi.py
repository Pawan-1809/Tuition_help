"""
ASGI config for Tuition Connect project.
"""

import os
from django.core.asgi import get_asgi_application
from django.core.management import call_command

if os.environ.get('RENDER'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django_asgi_app = get_asgi_application()

if os.environ.get('RENDER'):
    try:
        print("Executing automatic database migrations on boot...")
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Boot migration failed: {e}")

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.chat.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})
