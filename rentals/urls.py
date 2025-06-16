from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<int:car_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('rental/<int:rental_id>/', views.rental_detail, name='rental_detail'),
]

