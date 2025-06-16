from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('top-up/', views.top_up_balance, name='top_up_balance'),
    path('history/', views.purchase_history, name='purchase_history'),
]

