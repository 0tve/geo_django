from django import test, urls
from django.contrib.auth import models as auth_models
from django.contrib.gis import geos
from rest_framework import status
from rest_framework import test as drf_test
from rest_framework.authtoken import models as token_models

from . import models

USERNAME = 'testuser'
EMAIL = 'test@example.com'
PASSWORD = 'mypassword123'
LONGITUDE = 30.0
LATITUDE = 50.0
LATITUDE_FAR = 60.0
TEXT = 'test'
FORMAT = 'json'
SRID = 4326
POINT_DATA = {
    'type': 'Feature',
    'geometry': {
        'type': 'Point',
        'coordinates': [LONGITUDE, LATITUDE],
    },
    'properties': {}
}
GEO_PARAMS = {
    'latitude': LATITUDE,
    'longitude': LONGITUDE,
    'radius': 5,
}


class AuthTests(test.TestCase):
    def setUp(self):
        self.client = drf_test.APIClient()

    def test_register(self):
        url = urls.reverse('register')
        data = {
            'username': USERNAME,
            'email': EMAIL,
            'password': PASSWORD,
        }
        response = self.client.post(url, data, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(auth_models.User.objects.filter(
            username=USERNAME).exists())
        self.assertTrue(token_models.Token.objects.filter(
            key=response.data['token']).exists())

    def test_login(self):
        auth_models.User.objects.create_user(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD,
        )
        url = urls.reverse('login')
        response = self.client.post(
            url, {'username': USERNAME, 'password': PASSWORD}, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class PointTests(test.TestCase):
    def setUp(self):
        self.client = drf_test.APIClient()
        self.user = auth_models.User.objects.create_user(
            username=USERNAME, password=PASSWORD)
        self.token = token_models.Token.objects.create(user=self.user)
        self.auth_client = drf_test.APIClient()
        self.auth_client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_point_create_requires_auth(self):
        url = urls.reverse('point-create')
        response = self.client.post(url, POINT_DATA, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_point_create(self):
        url = urls.reverse('point-create')
        response = self.auth_client.post(url, POINT_DATA, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Point.objects.count(), 1)

    def test_point_search(self):
        models.Point.objects.create(
            location=geos.Point(LONGITUDE, LATITUDE, srid=SRID))
        models.Point.objects.create(location=geos.Point(
            LONGITUDE, LATITUDE_FAR, srid=SRID))
        url = urls.reverse('point-search')
        response = self.client.get(url, GEO_PARAMS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        features = response.data['features']
        self.assertEqual(len(features), 1)
        coords = features[0]['geometry']['coordinates']
        self.assertEqual(coords, [LONGITUDE, LATITUDE])

    def test_point_search_params(self):
        url = urls.reverse('point-search')
        resposne = self.client.get(url)
        self.assertEqual(resposne.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('latitude', resposne.data)
        self.assertIn('longitude', resposne.data)
        self.assertIn('radius', resposne.data)


class MessageTests(test.TestCase):
    def setUp(self):
        self.client = drf_test.APIClient()
        self.user = auth_models.User.objects.create_user(
            username=USERNAME, password=PASSWORD)
        self.token = token_models.Token.objects.create(user=self.user)
        self.auth_client = drf_test.APIClient()
        self.auth_client.credentials(
            HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.near_point = models.Point.objects.create(
            location=geos.Point(LONGITUDE, LATITUDE, srid=SRID))
        self.far_point = models.Point.objects.create(
            location=geos.Point(LONGITUDE, LATITUDE_FAR, srid=SRID))

    def test_message_create_auth(self):
        url = urls.reverse(
            'message-create', kwargs={'point_id': self.near_point.id})
        response = self.client.post(url, {'text': TEXT}, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_message_create(self):
        url = urls.reverse(
            'message-create', kwargs={'point_id': self.near_point.id})
        response = self.auth_client.post(url, {'text': TEXT}, format=FORMAT)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Message.objects.filter(
            point=self.near_point, text=TEXT).exists())

    def test_message_search(self):
        near_msg = models.Message.objects.create(
            point=self.near_point, text=TEXT)
        far_msg = models.Message.objects.create(
            point=self.far_point, text=TEXT)
        url = urls.reverse('message-search')
        response = self.client.get(url, GEO_PARAMS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [item['id'] for item in response.data]
        self.assertIn(near_msg.id, ids)
        self.assertNotIn(far_msg.id, ids)

    def test_message_search_params(self):
        url = urls.reverse('message-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('latitude', response.data)
        self.assertIn('longitude', response.data)
        self.assertIn('radius', response.data)
