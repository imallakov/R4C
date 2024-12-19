from django.urls import path

from .views import RobotView, download_robot_production_report

urlpatterns = [
    path('add/', RobotView.as_view(), name='add_robot'),
    path('download_report/', download_robot_production_report, name='download_report'),
]
