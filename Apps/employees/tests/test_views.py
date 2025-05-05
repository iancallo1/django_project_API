from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.tests.factories import UserFactory, EmployeeFactory, ManagerFactory
from employees.models import Employee

class EmployeeViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employee = EmployeeFactory()
        self.manager = ManagerFactory()
        self.regular_user = UserFactory()
        
        # URLs
        self.employee_list_url = reverse('employee-list')
        self.employee_detail_url = reverse('employee-detail', kwargs={'pk': self.employee.pk})
        self.employee_delete_url = reverse('employee-delete-employee', kwargs={'pk': self.employee.pk})

    def test_employee_list_unauthorized(self):
        """Test that unauthorized users cannot access employee list"""
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_list_authorized(self):
        """Test that managers can access employee list"""
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)

    def test_employee_detail_unauthorized(self):
        """Test that unauthorized users cannot access employee details"""
        response = self.client.get(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_employee_detail_authorized(self):
        """Test that managers can access employee details"""
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_username'], self.employee.user.username)

    def test_create_employee_unauthorized(self):
        """Test that unauthorized users cannot create employees"""
        data = {
            'username': 'newemployee',
            'email': 'new@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'first_name': 'New',
            'last_name': 'Employee',
            'join_date': '2024-01-01',
            'phone_number': '1234567890'
        }
        response = self.client.post(self.employee_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_employee_authorized(self):
        """Test that managers can create employees"""
        self.client.force_authenticate(user=self.manager)
        data = {
            'username': 'newemployee',
            'email': 'new@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'first_name': 'New',
            'last_name': 'Employee',
            'join_date': '2024-01-01',
            'phone_number': '1234567890'
        }
        response = self.client.post(self.employee_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user_username'], 'newemployee')

    def test_update_employee_unauthorized(self):
        """Test that unauthorized users cannot update employees"""
        data = {'phone_number': '9876543210'}
        response = self.client.patch(self.employee_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_employee_authorized(self):
        """Test that managers can update employees"""
        self.client.force_authenticate(user=self.manager)
        data = {'phone_number': '9876543210'}
        response = self.client.patch(self.employee_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], '9876543210')

    def test_delete_employee_unauthorized(self):
        """Test that unauthorized users cannot delete employees"""
        response = self.client.delete(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_employee_authorized(self):
        """Test that managers can delete employees"""
        self.client.force_authenticate(user=self.manager)
        response = self.client.delete(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Employee.objects.filter(pk=self.employee.pk).exists())

    def test_delete_employee_preview(self):
        """Test the delete preview action"""
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(self.employee_delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('employee', response.data)
        self.assertIn('warning', response.data)
        self.assertEqual(response.data['employee']['username'], self.employee.user.username)

    def test_regular_user_cannot_access_employee_list(self):
        """Test that regular users cannot access employee list"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 