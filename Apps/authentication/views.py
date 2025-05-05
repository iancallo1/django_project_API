from rest_framework import viewsets, permissions, routers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class APIRootView(APIView):
    def get(self, request, format=None):
        return Response({
            'employees': request.build_absolute_uri('employees/'),
            'leave-types': request.build_absolute_uri('leave-types/'),
            'leaves': request.build_absolute_uri('leaves/'),
            'leave-approvals': request.build_absolute_uri('leave-approvals/'),
        })

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get the current user's information
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data) 