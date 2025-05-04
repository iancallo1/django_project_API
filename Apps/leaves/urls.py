from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'leave-types', views.LeaveTypeViewSet)
router.register(r'leaves', views.LeaveViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 