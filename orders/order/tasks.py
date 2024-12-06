from celery import shared_task
from .models import Order



@shared_task
def update_order_total(order_id):
    """
    Асинхронно обновляет общую сумму заказа.
    """
    try:
        order = Order.objects.get(id=order_id)
        order.update_total_amount()  # Метод для пересчета суммы заказа
    except Order.DoesNotExist:
        # Логируем ошибку, если заказ не найден
        print(f"Order with ID {order_id} does not exist.")

