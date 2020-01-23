import datetime
from django.test import TestCase
from .models import StoredWebPages
from django.test import Client
from django.urls import reverse
from .service.webscraperservice import WebScraperService
from .service.storageservice import StorageService
from .serializers import StoredWebPagesSerializer, InputStoredWebPagesSerializer
from django.contrib.auth import get_user_model
from.exceptions import AddressAlreadyCheckedException


class ScraperUnitTest(TestCase):
    def setUp(self) -> None:
        self.dummy_address = 'www.google.com'
        self.client = Client()

        self.stored_attributes = {
            'address': self.dummy_address,
            'text_length': 1000,
            'images_number': 2,
            'status': True,
            'date_added': datetime.datetime.now()
        }

        self.stored_web = StoredWebPages.objects.create(**self.stored_attributes)
        self.serializer = StoredWebPagesSerializer(instance=self.stored_web)

    def test_login_fail(self):
        response = self.client.post(reverse('accounts:user_login'), {"username": "a", "password": "a"})
        self.assertTrue('Invalid login details given' in response.content.decode())

    def test_login_success(self):
        self.user = get_user_model().objects.create_user(username='b', password='b')
        self.user.save()
        response = self.client.post(reverse('accounts:user_login'), {"username": "b", "password": "b"}, follow=True)
        self.assertTrue('Logout' in response.content.decode())

    def test_register(self):
        response = self.client.post(reverse('accounts:register'), {"username": "c", "password": "c"}, follow=True)
        self.assertTrue('Thank you for registering' in response.content.decode())

    def test_scrape_fail(self):
        response = self.client.post(reverse('scraper-list'), {"address": self.dummy_address})
        self.assertTrue(response.status_code == 403)

    def test_scrape_success(self):
        service = WebScraperService()
        response = service.scrape_content(self.dummy_address)
        self.assertTrue('text' in response)

    def test_serializer_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['id', 'address', 'text_length', 'images_number', 'status', 'date_added'])

    def test_serializer_out_fields(self):
        data = self.serializer.data
        self.assertEqual(data['address'], self.stored_attributes['address'])

    def test_serializer_validate_fail(self):
        serializer = InputStoredWebPagesSerializer(data={'address': self.dummy_address})
        with self.assertRaises(AddressAlreadyCheckedException):
            valid = serializer.is_valid()

    def test_serializer_validate_success(self):
        StoredWebPages.objects.all().delete()
        serializer = InputStoredWebPagesSerializer(data={'address': self.dummy_address})
        valid = serializer.is_valid()
        self.assertTrue(valid)

    def test_post_to_get_data(self):
        self.user = get_user_model().objects.create_user(username='d', password='d')
        self.user.save()
        self.client.post(reverse('accounts:user_login'), {"username": "d", "password": "d"}, follow=True)
        StoredWebPages.objects.all().delete()
        response = self.client.post(reverse('scraper-list'), {"address": self.dummy_address}, follow=True)
        self.assertTrue('text' in response.content.decode())

    def test_save_retrieve(self):
        self.user = get_user_model().objects.create_user(username='e', password='e')
        self.user.save()
        self.client.post(reverse('accounts:user_login'), {"username": "e", "password": "e"}, follow=True)
        id = self.stored_web.id
        response = self.client.get(reverse('scraper-list'), {"pk": 1}, follow=True)
        self.assertTrue(self.dummy_address in response.content.decode())

    def test_storage_get_stored(self):
        id = self.stored_web.id
        service = StorageService()
        response = service.get_stored_content(id)
        self.assertTrue('images' in str(response))
