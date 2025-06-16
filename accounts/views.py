from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from rentals.models import Rental, Cart
from decimal import Decimal
from .forms import CustomUserCreationForm

User = get_user_model()


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """Личный кабинет пользователя"""
    user = request.user
    
    # Получаем историю аренды
    rentals = Rental.objects.filter(user=user).order_by('-created_at')
    
    # Получаем корзину
    cart_items = Cart.objects.filter(user=user)
    
    # Подсчитываем общую стоимость корзины
    cart_total = sum(item.total_price for item in cart_items)
    
    context = {
        'user': user,
        'rentals': rentals,
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'accounts/profile.html', context)


@login_required
def top_up_balance(request):
    """Пополнение баланса"""
    if request.method == 'POST':
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
            if amount > 0:
                with transaction.atomic():
                    user = User.objects.select_for_update().get(pk=request.user.pk)
                    user.balance += amount
                    user.save()
                    messages.success(request, f'Баланс пополнен на {amount} руб.')
            else:
                messages.error(request, 'Сумма должна быть положительной')
        except (ValueError, TypeError):
            messages.error(request, 'Неверная сумма')
    
    return redirect('profile')


@login_required
def purchase_history(request):
    """История покупок/аренды"""
    rentals = Rental.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'rentals': rentals,
    }
    
    return render(request, 'accounts/purchase_history.html', context)

