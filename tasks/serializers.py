from rest_framework import serializers
from tasks.models import Task, Goal
from accounts.models import CustomUser


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


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'name', 'price', 'is_achieved', 'progress']
        read_only_fields = ['is_achieved', 'progress']


class EmptySerializer(serializers.Serializer):
    pass
