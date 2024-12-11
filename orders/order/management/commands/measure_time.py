import time
from django.core.management.base import BaseCommand
from order.models import OrderItem, Order
from cacheops import invalidate_all

class Command(BaseCommand):
    help = 'Измеряет время выполнения запроса к базе данных'

    def handle(self, *args, **options):
        self.stdout.write("Очистка кэша...")
        invalidate_all()  # Полностью очищает кэш для точного сравнения

        # 1. Запрос без кэширования
        self.stdout.write("Измерение времени выполнения запроса без кэширования...")
        start = time.time()
        data = list(OrderItem.objects.all())  # Преобразуем QuerySet в список, чтобы данные были извлечены
        end = time.time()
        no_cache_time = end - start
        self.stdout.write(f"Время выполнения без кэширования: {no_cache_time:.4f} секунд")
        
        # 2. Запрос с кэшированием
        self.stdout.write("Измерение времени выполнения запроса с кэшированием...")
        start = time.time()
        data = list(OrderItem.objects.all())  # Повторяем тот же запрос, который теперь должен быть закэширован
        end = time.time()
        cache_time = end - start
        self.stdout.write(f"Время выполнения с кэшированием: {cache_time:.4f} секунд")

        # Сравнение
        self.stdout.write("Результаты измерений:")
        self.stdout.write(f"- Без кэширования: {no_cache_time:.4f} секунд")
        self.stdout.write(f"- С кэшированием: {cache_time:.4f} секунд")
        improvement = ((no_cache_time - cache_time) / no_cache_time) * 100 if no_cache_time > 0 else 0
        self.stdout.write(f"Ускорение за счёт кэширования: {improvement:.2f}%")
