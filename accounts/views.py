from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate, login, logout
from accounts.models import CustomUser
from accounts.serializers import RegistrationSerializer, ParentLoginSerializer, KidLoginSerializer, EmptySerializer
from accounts.permissions import IsAuthenticatedParent


class ParentRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.create_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            is_parent=True
        )
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Parent registered successfully"}, status=status.HTTP_201_CREATED, headers=headers)


class KidCreateView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticatedParent]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        kid = CustomUser.objects.create_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            parent=request.user  # Set the parent field
        )
        return Response({"message": "Kid account created successfully"}, status=status.HTTP_201_CREATED)


class ParentLoginView(GenericAPIView):
    serializer_class = ParentLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_parent:
            login(request, user)
            return Response({"message": "Successfully logged in"}, status=200)
        return Response({"error": "Invalid credentials"}, status=400)


class KidLoginView(GenericAPIView):
    serializer_class = KidLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if user is not None and not user.is_parent:
            login(request, user)
            return Response({"message": "Successfully logged in"}, status=200)
        return Response({"error": "Invalid credentials"}, status=400)


class LogoutView(GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=200)
