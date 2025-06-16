#!/usr/bin/env python3
"""
Скрипт для заполнения базы данных тестовыми автомобилями
"""

import os
import sys
import django

# Настройка Django
sys.path.append('/home/ubuntu/car_rental_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_rental_site.settings')
django.setup()

from cars.models import Car, CarImage

def create_cars():
    """Создание тестовых автомобилей"""
    
    cars_data = [
        {
            'brand': 'Toyota',
            'model': 'Camry',
            'year': 2020,
            'mileage': 25000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 3500.00,
            'price_per_week': 22000.00,
            'price_per_month': 85000.00,
            'description': 'Надежный и комфортабельный седан Toyota Camry 2020 года. Автоматическая коробка передач, кондиционер, навигация. Идеально подходит для деловых поездок и семейного отдыха.',
            'image': 'cars/toyota_camry_2020.jpg'
        },
        {
            'brand': 'BMW',
            'model': 'X5',
            'year': 2021,
            'mileage': 15000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 7500.00,
            'price_per_week': 48000.00,
            'price_per_month': 180000.00,
            'description': 'Премиальный кроссовер BMW X5 2021 года. Полный привод, кожаный салон, панорамная крыша, система безопасности. Роскошь и комфорт для особых случаев.',
            'image': 'cars/bmw_x5_2021.jpg'
        },
        {
            'brand': 'Mercedes-Benz',
            'model': 'C-Class',
            'year': 2022,
            'mileage': 8000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 6000.00,
            'price_per_week': 38000.00,
            'price_per_month': 145000.00,
            'description': 'Элегантный седан Mercedes-Benz C-Class 2022 года. Современные технологии, премиальный интерьер, отличная управляемость. Статус и комфорт в одном автомобиле.',
            'image': 'cars/mercedes_c_class_2022.jpg'
        },
        {
            'brand': 'Audi',
            'model': 'A4',
            'year': 2021,
            'mileage': 18000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 5500.00,
            'price_per_week': 35000.00,
            'price_per_month': 130000.00,
            'description': 'Спортивный седан Audi A4 2021 года. Quattro полный привод, спортивная подвеска, мультимедийная система. Динамичность и элегантность немецкого качества.',
            'image': 'cars/audi_a4_2021.jpg'
        },
        {
            'brand': 'Volkswagen',
            'model': 'Golf',
            'year': 2021,
            'mileage': 12000,
            'fuel_type': 'petrol',
            'transmission': 'manual',
            'price_per_day': 2800.00,
            'price_per_week': 18000.00,
            'price_per_month': 68000.00,
            'description': 'Компактный хэтчбек Volkswagen Golf 2021 года. Экономичный расход топлива, удобная парковка в городе, надежность. Отличный выбор для городских поездок.',
            'image': 'cars/volkswagen_golf_2021.jpg'
        },
        {
            'brand': 'Volkswagen',
            'model': 'Golf',
            'year': 2021,
            'mileage': 10000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 3200.00,
            'price_per_week': 20000.00,
            'price_per_month': 75000.00,
            'description': 'Белый Volkswagen Golf 2021 года с автоматической коробкой передач. Стильный дизайн, современные технологии, экономичность. Идеален для ежедневного использования.',
            'image': 'cars/volkswagen_golf_white_2021.jpg'
        },
        {
            'brand': 'Honda',
            'model': 'Civic',
            'year': 2020,
            'mileage': 22000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 3000.00,
            'price_per_week': 19000.00,
            'price_per_month': 72000.00,
            'description': 'Надежный седан Honda Civic 2020 года. Просторный салон, экономичный двигатель, отличная репутация надежности. Практичный выбор для любых задач.',
            'image': 'cars/toyota_camry_2020.jpg'  # Используем имеющееся изображение
        },
        {
            'brand': 'Hyundai',
            'model': 'Elantra',
            'year': 2021,
            'mileage': 16000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 2900.00,
            'price_per_week': 18500.00,
            'price_per_month': 70000.00,
            'description': 'Современный седан Hyundai Elantra 2021 года. Стильный дизайн, богатая комплектация, гарантия качества. Комфорт и надежность по доступной цене.',
            'image': 'cars/audi_a4_2021.jpg'  # Используем имеющееся изображение
        },
        {
            'brand': 'Kia',
            'model': 'Rio',
            'year': 2020,
            'mileage': 28000,
            'fuel_type': 'petrol',
            'transmission': 'manual',
            'price_per_day': 2200.00,
            'price_per_week': 14000.00,
            'price_per_month': 52000.00,
            'description': 'Экономичный хэтчбек Kia Rio 2020 года. Низкий расход топлива, компактные размеры, доступная цена. Отличный вариант для начинающих водителей.',
            'image': 'cars/volkswagen_golf_2021.jpg'  # Используем имеющееся изображение
        },
        {
            'brand': 'Mazda',
            'model': 'CX-5',
            'year': 2021,
            'mileage': 14000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 4500.00,
            'price_per_week': 28000.00,
            'price_per_month': 105000.00,
            'description': 'Стильный кроссовер Mazda CX-5 2021 года. Полный привод, премиальный интерьер, отличная управляемость. Японское качество и надежность.',
            'image': 'cars/bmw_x5_2021.jpg'  # Используем имеющееся изображение
        },
        {
            'brand': 'Nissan',
            'model': 'Qashqai',
            'year': 2020,
            'mileage': 20000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 4000.00,
            'price_per_week': 25000.00,
            'price_per_month': 95000.00,
            'description': 'Популярный кроссовер Nissan Qashqai 2020 года. Просторный салон, высокая посадка, современные технологии. Универсальность для города и путешествий.',
            'image': 'cars/bmw_x5_2021.jpg'  # Используем имеющееся изображение
        },
        {
            'brand': 'Ford',
            'model': 'Focus',
            'year': 2020,
            'mileage': 24000,
            'fuel_type': 'petrol',
            'transmission': 'manual',
            'price_per_day': 2700.00,
            'price_per_week': 17000.00,
            'price_per_month': 64000.00,
            'description': 'Динамичный хэтчбек Ford Focus 2020 года. Спортивная управляемость, современный дизайн, надежность. Европейское качество по разумной цене.',
            'image': 'cars/volkswagen_golf_2021.jpg'  # Используем имеющееся изображение
        },
        {
            'brand': 'Skoda',
            'model': 'Octavia',
            'year': 2021,
            'mileage': 11000,
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'price_per_day': 3300.00,
            'price_per_week': 21000.00,
            'price_per_month': 78000.00,
            'description': 'Практичный седан Skoda Octavia 2021 года. Просторный багажник, экономичность, чешское качество. Идеальный баланс цены и качества.',
            'image': 'cars/audi_a4_2021.jpg'  # Используем имеющееся изображение
        },
        {
            'brand': 'Renault',
            'model': 'Logan',
            'year': 2020,
            'mileage': 30000,
            'fuel_type': 'petrol',
            'transmission': 'manual',
            'price_per_day': 2000.00,
            'price_per_week': 12500.00,
            'price_per_month': 47000.00,
            'description': 'Бюджетный седан Renault Logan 2020 года. Низкая стоимость обслуживания, простота и надежность. Экономичный вариант для повседневных поездок.',
            'image': 'cars/toyota_camry_2020.jpg'  # Используем имеющееся изображение
        },
        {
            'brand': 'Lada',
            'model': 'Vesta',
            'year': 2021,
            'mileage': 8000,
            'fuel_type': 'petrol',
            'transmission': 'manual',
            'price_per_day': 2100.00,
            'price_per_week': 13000.00,
            'price_per_month': 49000.00,
            'description': 'Отечественный седан Lada Vesta 2021 года. Современный дизайн, доступная цена, простое обслуживание. Патриотичный выбор с хорошим соотношением цена-качество.',
            'image': 'cars/audi_a4_2021.jpg'  # Используем имеющееся изображение
        }
    ]
    
    print("Создание автомобилей...")
    
    for car_data in cars_data:
        # Извлекаем данные изображения
        image_path = car_data.pop('image')
        
        # Создаем автомобиль
        car, created = Car.objects.get_or_create(
            brand=car_data['brand'],
            model=car_data['model'],
            year=car_data['year'],
            defaults=car_data
        )
        
        if created:
            print(f"Создан автомобиль: {car}")
            
            # Создаем изображение для автомобиля
            car_image, img_created = CarImage.objects.get_or_create(
                car=car,
                image=image_path,
                defaults={'is_main': True}
            )
            
            if img_created:
                print(f"  Добавлено изображение: {image_path}")
        else:
            print(f"Автомобиль уже существует: {car}")
    
    print(f"\nВсего автомобилей в базе: {Car.objects.count()}")

if __name__ == '__main__':
    create_cars()

