from django.test import TestCase
from .models import OrderItem, OrderProduct, Order
import time


class PerformanceTest(TestCase):
    def test_query_performance(self):
        start = time.time()
        OrderItem.objects.all()
        end = time.time()
        print(f"Время выполнения запроса: {end - start} секунд")


class PerformanceTest1(TestCase):
    def test_query_performance(self):
        start = time.time()
        OrderProduct.objects.all()
        end = time.time()
        print(f"Время выполнения запроса: {end - start} секунд")


class PerformanceTest2(TestCase):
    def test_query_performance(self):
        start = time.time()
        Order.objects.all()
        end = time.time()
        print(f"Время выполнения запроса: {end - start} секунд")

