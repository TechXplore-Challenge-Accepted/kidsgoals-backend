import requests
from django.core.exceptions import PermissionDenied
from djoser.email import ActivationEmail
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from accounts.serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class ActivateUser(APIView):
    """
    After following the activation link the user will be activated automatically.
    """
    permission_classes = [AllowAny]

    def get(self, request, uid, token, format=None):
        payload = {'uid': uid, 'token': token}
        url = f"{request.scheme}://{request.get_host()}/api/auth/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({"message": "Your account has been activated!"}, status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)


class ParentRegisterView(generics.CreateAPIView):
    """
    Parents can register with this view to create their account.
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_parent=True)
        user.is_active = False  # Ensure the user is inactive until they activate their account
        user.save()

        # Send the activation email
        context = {'user': user}
        to = [user.email]
        ActivationEmail(context=context).send(to)


class KidRegisterView(generics.CreateAPIView):
    """
    This view is used by parents to create their kid accounts. Parent must be authenticated to create kid accounts.
    """
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_parent:
            raise PermissionDenied("Only parents can create kid accounts")
        kid = serializer.save(is_parent=False, parent=self.request.user)
        kid.is_active = False  # Ensure the kid is inactive until they activate their account
        kid.save()

        # Send the activation email
        context = {'user': kid}
        to = [kid.email]
        ActivationEmail(context=context).send(to)


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


