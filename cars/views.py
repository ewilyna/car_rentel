from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Car


def car_list(request):
    """Список автомобилей с фильтрацией и поиском"""
    cars = Car.objects.filter(is_available=True).order_by('-created_at')
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        cars = cars.filter(
            Q(brand__icontains=search_query) |
            Q(model__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Фильтры
    brand_filter = request.GET.get('brand', '')
    if brand_filter:
        cars = cars.filter(brand__icontains=brand_filter)
    
    fuel_filter = request.GET.get('fuel_type', '')
    if fuel_filter:
        cars = cars.filter(fuel_type=fuel_filter)
    
    transmission_filter = request.GET.get('transmission', '')
    if transmission_filter:
        cars = cars.filter(transmission=transmission_filter)
    
    year_from = request.GET.get('year_from', '')
    if year_from:
        try:
            cars = cars.filter(year__gte=int(year_from))
        except ValueError:
            pass
    
    year_to = request.GET.get('year_to', '')
    if year_to:
        try:
            cars = cars.filter(year__lte=int(year_to))
        except ValueError:
            pass
    
    price_from = request.GET.get('price_from', '')
    if price_from:
        try:
            cars = cars.filter(price_per_day__gte=float(price_from))
        except ValueError:
            pass
    
    price_to = request.GET.get('price_to', '')
    if price_to:
        try:
            cars = cars.filter(price_per_day__lte=float(price_to))
        except ValueError:
            pass
    
    mileage_from = request.GET.get('mileage_from', '')
    if mileage_from:
        try:
            cars = cars.filter(mileage__gte=int(mileage_from))
        except ValueError:
            pass
    
    mileage_to = request.GET.get('mileage_to', '')
    if mileage_to:
        try:
            cars = cars.filter(mileage__lte=int(mileage_to))
        except ValueError:
            pass
    
    # Сортировка
    sort_by = request.GET.get('sort', 'created_at')
    if sort_by == 'price_asc':
        cars = cars.order_by('price_per_day')
    elif sort_by == 'price_desc':
        cars = cars.order_by('-price_per_day')
    elif sort_by == 'year_asc':
        cars = cars.order_by('year')
    elif sort_by == 'year_desc':
        cars = cars.order_by('-year')
    elif sort_by == 'mileage_asc':
        cars = cars.order_by('mileage')
    elif sort_by == 'mileage_desc':
        cars = cars.order_by('-mileage')
    else:
        cars = cars.order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(cars, 12)  # 12 автомобилей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем уникальные марки для фильтра
    brands = Car.objects.values_list('brand', flat=True).distinct().order_by('brand')
    
    context = {
        'page_obj': page_obj,
        'brands': brands,
        'search_query': search_query,
        'current_filters': {
            'brand': brand_filter,
            'fuel_type': fuel_filter,
            'transmission': transmission_filter,
            'year_from': year_from,
            'year_to': year_to,
            'price_from': price_from,
            'price_to': price_to,
            'mileage_from': mileage_from,
            'mileage_to': mileage_to,
            'sort': sort_by,
        }
    }
    
    return render(request, 'cars/car_list.html', context)


def car_detail(request, pk):
    """Детальная страница автомобиля"""
    car = get_object_or_404(Car, pk=pk, is_available=True)
    
    context = {
        'car': car,
    }
    
    return render(request, 'cars/car_detail.html', context)

