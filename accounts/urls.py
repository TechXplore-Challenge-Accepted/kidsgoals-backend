from django.urls import path
from accounts.views import ActivateUser, ParentRegisterView, KidRegisterView, LogoutView

urlpatterns = [
    path('parent/register/', ParentRegisterView.as_view(), name='parent-register'),
    path('kid/register/', KidRegisterView.as_view(), name='kid-register'),
    path('activate/<uid>/<token>/', ActivateUser.as_view(), name='activate-user'),
    path('activate/', ActivateUser.as_view(), name='activate-user'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

