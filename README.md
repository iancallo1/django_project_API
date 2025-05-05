# Django Authentication API

A robust authentication system built with Django and Django REST Framework, providing user management and authentication features for your application.

## Features

- Custom User Model with extended fields
- User registration and authentication
- Role-based access control (Employee and Manager roles)
- RESTful API endpoints for user management
- Password validation and confirmation
- Secure password handling
- Comprehensive test coverage

## Prerequisites

- Python 3.14.0
- Django 5.2
- Django REST Framework
- Virtual environment (recommended)

## What I have Learned


## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd django_project2
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

## API Endpoints

### Authentication

- `POST /api/users/` - Register a new user
- `GET /api/users/` - List all users (requires authentication)
- `GET /api/users/{id}/` - Get user details (requires authentication)
- `PUT /api/users/{id}/` - Update user details (requires authentication)
- `DELETE /api/users/{id}/` - Delete user (requires authentication)
- `GET /api/users/me/` - Get current user's information (requires authentication)

### User Model Fields

- `username` - Unique username
- `email` - Email address
- `first_name` - First name
- `last_name` - Last name
- `is_employee` - Employee role flag
- `is_manager` - Manager role flag
- `password` - Password (write-only)
- `confirm_password` - Password confirmation (write-only)

## Usage Examples

### Register a New User

```python
POST /api/users/
{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123",
    "confirm_password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "is_employee": true,
    "is_manager": false
}
```

### Get Current User Information

```python
GET /api/users/me/
Headers: {
    "Authorization": "Token your-auth-token"
}
```

## Testing

Run the test suite:
```bash
python manage.py test authentication
```
```bash
python manage.py test Apps.employees.tests.test_views
```
## Security Features

- Password validation using Django's built-in validators
- Password confirmation during registration
- Token-based authentication
- Role-based access control
- Secure password storage using Django's password hashing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is open sourced feel free to contribute.
