import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from employees.models import Employee

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_employee = False
    is_manager = False

class EmployeeFactory(DjangoModelFactory):
    class Meta:
        model = Employee

    user = factory.SubFactory(UserFactory, is_employee=True)
    join_date = factory.Faker('date')
    phone_number = factory.Faker('phone_number')

class ManagerFactory(UserFactory):
    is_manager = True 