from django.test import TestCase
from rest_framework.exceptions import ValidationError
from .factories import UserFactory
from ..serializers import UserSerializer

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'is_employee': False,
            'is_manager': False
        }

    def test_create_user(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_password_mismatch(self):
        self.user_data['confirm_password'] = 'differentpass'
        serializer = UserSerializer(data=self.user_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_serialize_existing_user(self):
        user = UserFactory()
        serializer = UserSerializer(user)
        data = serializer.data
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['email'], user.email)
        self.assertNotIn('password', data)
        self.assertNotIn('confirm_password', data) 