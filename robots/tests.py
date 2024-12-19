from django.test import TestCase, Client
from django.urls import reverse
import json
from .models import Robot

class RobotViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        Robot.objects.create(serial="R2-D2", model="R2", version="D2", created="2022-12-31 23:59:59")

    def test_add_robot_post(self):
        url = reverse('add_robot')
        data = {"model": "R2", "version": "D2", "created": "2023-01-01 00:00:00"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Robot.objects.count(), 2)

    def test_add_robot_invalid_data(self):
        url = reverse('add_robot')
        data = {"model": "R8", "version": "D2", "created": "2023-01-01 00:00:00"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Такой модели роботов не существует.", response.json().get('error'))


    def test_method_not_allowed(self):
        url = reverse('add_robot')
        response = self.client.put(url, {}, content_type='application/json')
        self.assertEqual(response.status_code, 405)