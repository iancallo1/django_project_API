from django.test import TestCase
from django.contrib.auth import get_user_model
from .factories import UserFactory, EmployeeFactory, ManagerFactory

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = UserFactory()
        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_employee)
        self.assertFalse(user.is_manager)

    def test_create_employee(self):
        employee = EmployeeFactory()
        self.assertTrue(employee.is_employee)
        self.assertFalse(employee.is_manager)
        self.assertTrue(employee.check_password('testpass123'))

    def test_create_manager(self):
        manager = ManagerFactory()
        self.assertTrue(manager.is_manager)
        self.assertFalse(manager.is_employee)
        self.assertTrue(manager.check_password('testpass123'))

    def test_user_str_method(self):
        user = UserFactory(username='testuser')
        self.assertEqual(str(user), 'testuser') 