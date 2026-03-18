# URLs ki routing yahan par hai

"""
Dashboard URL Configuration
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.analytics_view, name='analytics'),
    path('api/charts/', views.chart_data_api, name='chart_data'),
    path('users/<str:role>/', views.manage_users_view, name='manage_users'),
    path('delete-user/<int:user_id>/', views.delete_user_api, name='delete_user'),
]
