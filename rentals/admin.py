from django.contrib import admin
from .models import Rental, Cart


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """Админ-панель для аренды"""
    list_display = ('user', 'car', 'start_date', 'end_date', 'total_price', 'status')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('user__username', 'car__brand', 'car__model')
    list_editable = ('status',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'car')
        }),
        ('Даты аренды', {
            'fields': ('start_date', 'end_date')
        }),
        ('Стоимость и статус', {
            'fields': ('total_price', 'status')
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Админ-панель для корзины"""
    list_display = ('user', 'car', 'start_date', 'end_date', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'car__brand', 'car__model')

