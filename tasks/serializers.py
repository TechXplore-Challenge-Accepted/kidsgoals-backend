from rest_framework import serializers
from .models import Task
from accounts.models import CustomUser
from .validators import validate_assigned_to


class EmptySerializer(serializers.Serializer):
    pass


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.none())

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'value', 'is_completed', 'is_approved', 'created_by', 'assigned_to']
        read_only_fields = ['is_completed', 'is_approved', 'created_by']

    def __init__(self, *args, **kwargs):
        super(TaskSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            if request.user.is_parent:
                self.fields['assigned_to'].queryset = CustomUser.objects.filter(parent=request.user)

