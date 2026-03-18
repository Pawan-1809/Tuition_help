# URLs ki routing yahan par hai

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_inbox, name='inbox'),
    path('tutor/<int:tutor_id>/', views.chat_with_tutor, name='chat_with_tutor'),
    path('room/<int:thread_id>/', views.chat_room, name='room'),
]
