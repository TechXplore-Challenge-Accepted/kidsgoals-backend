from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, GoalViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'goal', GoalViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),
]
