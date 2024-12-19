from django.shortcuts import render, redirect
from django.contrib import messages

from customers.models import Customer
from .forms import OrderForm
from robots.models import Robot


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            robot_model = form.cleaned_data['model']
            robot_version = form.cleaned_data['version']
            try:
                robots = Robot.objects.filter(model=robot_model, version=robot_version).order_by('created')
                if robots.exists():
                    first_robot = robots.first()
                    first_robot.delete()
                    message = "Ваш заказ обрабатывается!"
                    customer = Customer(email=message)
                    customer.save()
                else:
                    message = "Роботов данной модели пока нету в наличии! Мы уведомим вас как только появятся)"
                    order = form.save(message)

                messages.info(request, message)
                return redirect('order_result_page')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('order_result_page')
    else:
        form = OrderForm()
    return render(request, 'order_page', {'form': form})
