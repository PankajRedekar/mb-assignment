from rest_framework.test import APITestCase
from django.urls import reverse

from api import models
from api import serializers

class MangerUserCerateAPITest(APITestCase):
    url = reverse('api:signup')

    def test_create_manageruser(self):
        data = {
            "first_name":"Pankaj",
            "last_name":"r",
            "email":"admin@admin1.com",
            "password":"admin",
            "password1":"admin"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)