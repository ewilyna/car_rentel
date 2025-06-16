from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from cars.models import Car
from .models import Cart, Rental
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def add_to_cart(request, car_id):
    """Добавление автомобиля в корзину"""
    car = get_object_or_404(Car, pk=car_id, is_available=True)
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            # Проверяем даты
            if start_date < timezone.now().date():
                messages.error(request, 'Дата начала не может быть в прошлом')
                return redirect('car_detail', pk=car_id)
            
            if end_date <= start_date:
                messages.error(request, 'Дата окончания должна быть позже даты начала')
                return redirect('car_detail', pk=car_id)
            
            # Проверяем, нет ли уже этого автомобиля в корзине
            existing_cart_item = Cart.objects.filter(user=request.user, car=car).first()
            if existing_cart_item:
                # Обновляем даты
                existing_cart_item.start_date = start_date
                existing_cart_item.end_date = end_date
                existing_cart_item.save()
                messages.success(request, 'Даты аренды обновлены в корзине')
            else:
                # Создаем новый элемент корзины
                Cart.objects.create(
                    user=request.user,
                    car=car,
                    start_date=start_date,
                    end_date=end_date
                )
                messages.success(request, 'Автомобиль добавлен в корзину')
            
            return redirect('profile')
            
        except ValueError:
            messages.error(request, 'Неверный формат даты')
            return redirect('car_detail', pk=car_id)
    
    return redirect('car_detail', pk=car_id)


@login_required
def remove_from_cart(request, cart_id):
    """Удаление из корзины"""
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Автомобиль удален из корзины')
    return redirect('profile')


@login_required
def checkout(request):
    """Оформление аренды"""
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items:
        messages.error(request, 'Корзина пуста')
        return redirect('profile')
    
    # Подсчитываем общую стоимость
    total_cost = sum(item.total_price for item in cart_items)
    
    if request.user.balance < total_cost:
        messages.error(request, 'Недостаточно средств на балансе')
        return redirect('profile')
    
    # Создаем аренды и списываем деньги
    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=request.user.pk)
        
        # Проверяем баланс еще раз
        if user.balance < total_cost:
            messages.error(request, 'Недостаточно средств на балансе')
            return redirect('profile')
        
        # Создаем аренды
        for cart_item in cart_items:
            Rental.objects.create(
                user=user,
                car=cart_item.car,
                start_date=cart_item.start_date,
                end_date=cart_item.end_date,
                total_price=cart_item.total_price,
                status='confirmed'
            )
        
        # Списываем деньги
        user.balance -= total_cost
        user.save()
        
        # Очищаем корзину
        cart_items.delete()
        
        messages.success(request, f'Аренда оформлена! Списано {total_cost} руб.')
    
    return redirect('profile')


@login_required
def rental_detail(request, rental_id):
    """Детали аренды"""
    rental = get_object_or_404(Rental, pk=rental_id, user=request.user)
    
    context = {
        'rental': rental,
    }
    
    return render(request, 'rentals/rental_detail.html', context)

