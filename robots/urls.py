from django.urls import path
from .views import RobotView

urlpatterns = [
    path('add/', RobotView.as_view(), name='add_robot')
]