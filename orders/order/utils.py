from django.core.mail import send_mail

def send_order_confirmation_email(order):

    """
    Отправляет email с подтверждением заказа.
    """

    subject = f"Подтверждение заказа #{order.id}"
    message = (
        f"Здравствуйте, {order.customer.first_name}!\n\n"
        f"Ваш заказ #{order.id} был подтвержден.\n"
        f"Список товаров:\n"
    )
    
    for item in order.orderproduct_set.all():
        message += f"- {item.product.name} (количество: {item.quantity})\n"

    message += (
        "\nСпасибо за ваш заказ!\n"
        "С уважением, команда магазина."
    )

    send_mail(
        subject,
        message,
        'no-reply@example.com',  # Отправитель
        [order.customer.email],  # Получатель
    )


def send_order_cancellation_email(order):
    subject = f"Подтверждение заказа #{order.id} отменено"
    message = (
        f"Здравствуйте, {order.customer.first_name}!\n\n"
        f"Ваш заказ #{order.id} был переведён в статус 'ожидание'.\n"
        "Если у вас есть вопросы, свяжитесь с нами.\n\n"
        "С уважением, команда магазина."
    )
    send_mail(
        subject,
        message,
        'no-reply@example.com',
        [order.customer.email],
    )
