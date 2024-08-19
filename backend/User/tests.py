from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from rest_framework import status

from .serializers import UserInputSerializer, UserOutputSerializer


class UserListViewTests(TestCase):
    def setUp(self):
        self.url = '/users/'

    @patch('User.serializers.UserInputSerializer')
    @patch('User.serializers.UserOutputSerializer')
    def test_post_valid_data(self, mock_output_serializer, mock_input_serializer):
        # Mocking serializers
        input_serializer_instance = mock_input_serializer.return_value
        input_serializer_instance.is_valid.return_value = True
        input_serializer_instance.validated_data = {
            'username': 'testuser', 
            'password': 'password123'
        }

        output_serializer_instance = mock_output_serializer.return_value
        output_serializer_instance.data = {'id': 1, 'username': 'testuser'}

        response = self.client.post(
            self.url, 
            {'username': 'testuser', 'password': 'password123'}, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, output_serializer_instance.data)

    @patch('User.serializers.UserInputSerializer')
    def test_post_invalid_data(self, mock_input_serializer):
        # Mocking the invalid serializer
        input_serializer_instance = mock_input_serializer.return_value
        input_serializer_instance.is_valid.return_value = False
        input_serializer_instance.errors = {
            'username': ['This field is required.'], 
            'password': ['This field is required.']
        }

        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, input_serializer_instance.errors)

class UserManagerTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        username = 'user'
        password = 'password123'
        user = User.objects.create_user(username, password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_create_user_missing_username(self):
        User = get_user_model()
        password = 'password123'
        with self.assertRaises(ValueError):
            User.objects.create_user('', password)  # Missing username

    def test_create_user_missing_password(self):
        User = get_user_model()
        username = 'user'
        with self.assertRaises(ValueError):
            User.objects.create_user(username, '')  # Missing password

    def test_create_user_invalid_extra_fields(self):
        User = get_user_model()
        username = 'user'
        password = 'password123'
        extra_fields = {'invalid_field': 'value'}  # invalid extra field
        with self.assertRaises(TypeError):
            User.objects.create_user(username, password, **extra_fields)

    def test_create_superuser(self):
        User = get_user_model()
        username = 'admin'
        password = 'password123'
        superuser = User.objects.create_superuser(username, password)

        self.assertEqual(superuser.username, username)
        self.assertTrue(superuser.is_superuser)

    def test_create_superuser_with_extra_fields_throws(self):
        User = get_user_model()
        username = 'admin'
        password = 'password123'
        extra_fields = {'email': 'admin@example.com'}  # example extra fields
        with self.assertRaises(TypeError):
            User.objects.create_superuser(username, password, **extra_fields)

    def test_create_superuser_invalid_superuser_flag(self):
        User = get_user_model()
        username = 'admin'
        password = 'password123'
        extra_fields = {'is_superuser': False}  # setting is_superuser=False which is invalid for a superuser
        with self.assertRaises(ValueError):
            User.objects.create_superuser(username, password, **extra_fields)
