from django.db import models
from django.conf import settings
from cars.models import Car


class Rental(models.Model):
    """Модель аренды автомобиля"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждена'),
        ('active', 'Активна'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name="Автомобиль"
    )
    start_date = models.DateField(verbose_name="Дата начала аренды")
    end_date = models.DateField(verbose_name="Дата окончания аренды")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Аренда {self.car} - {self.user.username}"
    
    @property
    def duration_days(self):
        """Количество дней аренды"""
        return (self.end_date - self.start_date).days + 1


class Cart(models.Model):
    """Модель корзины"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name="Автомобиль"
    )
    start_date = models.DateField(verbose_name="Дата начала аренды")
    end_date = models.DateField(verbose_name="Дата окончания аренды")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        unique_together = ['user', 'car']
    
    def __str__(self):
        return f"Корзина {self.user.username} - {self.car}"
    
    @property
    def duration_days(self):
        """Количество дней аренды"""
        return (self.end_date - self.start_date).days + 1
    
    @property
    def total_price(self):
        """Общая стоимость"""
        days = self.duration_days
        if days >= 30:
            return self.car.price_per_month * (days // 30) + self.car.price_per_day * (days % 30)
        elif days >= 7:
            return self.car.price_per_week * (days // 7) + self.car.price_per_day * (days % 7)
        else:
            return self.car.price_per_day * days

