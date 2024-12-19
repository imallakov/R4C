from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Robot
from orders.models import Order
from customers.models import Customer


@receiver(post_save, sender=Robot)
def notify_customer_on_availability(sender, instance, created, **kwargs):
    if created:
        matching_orders = Order.objects.filter(robot_serial__startswith=f"{instance.model}-{instance.version}")

        for order in matching_orders:
            email = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {instance.model}, версии {instance.version}.\n\
                        Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
            customer = order.customer
            customer.email = email
            customer.save()
            order.delete()
