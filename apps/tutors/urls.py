# URLs ki routing yahan par hai

"""
Tutors URL Configuration
"""

from django.urls import path
from . import views

app_name = 'tutors'

urlpatterns = [

    path('', views.directory_view, name='directory'),

    path('<int:pk>/', views.tutor_detail_view, name='detail'),
    path('<int:pk>/review/', views.submit_review, name='submit_review'),

    path('api/search/', views.tutor_search_api, name='search_api'),
]
