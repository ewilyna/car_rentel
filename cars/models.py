from django.db import models
from django.urls import reverse


class Car(models.Model):
    """Модель автомобиля"""
    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('electric', 'Электро'),
        ('hybrid', 'Гибрид'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Механическая'),
        ('automatic', 'Автоматическая'),
    ]
    
    brand = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Год выпуска")
    mileage = models.IntegerField(verbose_name="Пробег (км)")
    fuel_type = models.CharField(
        max_length=20, 
        choices=FUEL_CHOICES, 
        default='petrol',
        verbose_name="Тип топлива"
    )
    transmission = models.CharField(
        max_length=20, 
        choices=TRANSMISSION_CHOICES, 
        default='manual',
        verbose_name="Коробка передач"
    )
    price_per_day = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        verbose_name="Цена за день (руб.)"
    )
    price_per_week = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        verbose_name="Цена за неделю (руб.)"
    )
    price_per_month = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        verbose_name="Цена за месяц (руб.)"
    )
    description = models.TextField(verbose_name="Описание")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'pk': self.pk})


class CarImage(models.Model):
    """Модель изображений автомобиля"""
    car = models.ForeignKey(
        Car, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name="Автомобиль"
    )
    image = models.ImageField(
        upload_to='cars/',
        verbose_name="Изображение"
    )
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")
    
    class Meta:
        verbose_name = "Изображение автомобиля"
        verbose_name_plural = "Изображения автомобилей"
    
    def __str__(self):
        return f"Изображение {self.car}"

