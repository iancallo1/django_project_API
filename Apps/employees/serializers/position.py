from rest_framework import serializers
from ..models import Position, Department
from .department import DepartmentSerializer

class PositionSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        source='department',
        write_only=True
    )

    class Meta:
        model = Position
        fields = ['id', 'name', 'department', 'department_id', 'description'] 