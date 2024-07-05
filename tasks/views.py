from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from tasks.models import Task, Goal
from tasks.serializers import TaskSerializer, EmptySerializer, GoalSerializer
from tasks.validators import validate_assigned_to, validate_task_completion, validate_task_approval
from accounts.permissions import IsAuthenticatedParent


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'approve_task']:
            return [permissions.IsAuthenticated(), IsAuthenticatedParent()]
        elif self.action in ['complete_task']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_parent:
            return Task.objects.filter(created_by=user)
        return Task.objects.filter(assigned_to=user)

    def perform_create(self, serializer):
        assigned_to = serializer.validated_data.get('assigned_to')
        validate_assigned_to(assigned_to, self.request.user)
        serializer.save(created_by=self.request.user)

    @action(detail=True, serializer_class=EmptySerializer, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def complete_task(self, request, pk=None):
        task = self.get_object()
        validate_task_completion(task, request.user)
        task.is_completed = True
        task.save()
        return Response({'status': 'task completed'})

    @action(detail=True, serializer_class=EmptySerializer, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsAuthenticatedParent])
    def approve_task(self, request, pk=None):
        task = self.get_object()
        validate_task_approval(task, request.user)
        task.is_approved = True
        task.assigned_to.balance += task.value
        task.assigned_to.save()
        task.save()
        return Response({'status': 'task approved'})


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_parent:
            return Goal.objects.filter(kid__parent=user)
        return Goal.objects.filter(kid=user)

    def create(self, request, *args, **kwargs):
        if request.user.is_parent:
            return Response({'detail': 'Parents cannot create goals.'}, status=status.HTTP_403_FORBIDDEN)

        if Goal.objects.filter(kid=request.user, is_achieved=False).exists():
            return Response({'detail': 'You already have an active goal.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(kid=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
