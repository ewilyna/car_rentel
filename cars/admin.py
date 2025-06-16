from django.contrib import admin
from .models import Car, CarImage


class CarImageInline(admin.TabularInline):
    """Инлайн для изображений автомобиля"""
    model = CarImage
    extra = 1


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    """Админ-панель для автомобилей"""
    list_display = ('brand', 'model', 'year', 'mileage', 'price_per_day', 'is_available')
    list_filter = ('brand', 'fuel_type', 'transmission', 'is_available', 'year')
    search_fields = ('brand', 'model', 'description')
    list_editable = ('is_available',)
    inlines = [CarImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('brand', 'model', 'year', 'mileage')
        }),
        ('Технические характеристики', {
            'fields': ('fuel_type', 'transmission')
        }),
        ('Цены', {
            'fields': ('price_per_day', 'price_per_week', 'price_per_month')
        }),
        ('Описание и доступность', {
            'fields': ('description', 'is_available')
        }),
    )


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    """Админ-панель для изображений автомобилей"""
    list_display = ('car', 'is_main')
    list_filter = ('is_main',)
    search_fields = ('car__brand', 'car__model')

