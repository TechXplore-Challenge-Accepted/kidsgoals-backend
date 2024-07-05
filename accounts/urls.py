from django.urls import path
from .views import ParentRegisterView, KidCreateView, ParentLoginView, KidLoginView, LogoutView

urlpatterns = [
    path('register/', ParentRegisterView.as_view(), name='register'),
    path('login/parent/', ParentLoginView.as_view(), name='parent_login'),
    path('login/kid/', KidLoginView.as_view(), name='kid_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('kids/', KidCreateView.as_view(), name='register_kid'),
]
