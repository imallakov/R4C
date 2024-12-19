from django import forms

from customers.models import Customer
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []

    model = forms.CharField(max_length=2, label='Модель')
    version = forms.CharField(max_length=2, label='Версия')

    def save(self, message, commit=True):
        order = Order()
        order.robot_serial = f"{self.cleaned_data['model']}-{self.cleaned_data['version']}"
        customer = Customer(email=message)
        customer.save()
        order.customer = customer
        if commit:
            order.save()
        return order
