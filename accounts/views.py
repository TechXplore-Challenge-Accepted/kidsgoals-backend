from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser
from .permissions import IsAuthenticatedParent
from .serializers import ParentSerializer, KidSerializer, ParentWithKidsSerializer, ParentLoginSerializer, KidLoginSerializer

class ParentRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            personal_id=serializer.validated_data['personal_id'],
            is_parent=True
        )
        user.save()
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Parent registered successfully"}, status=status.HTTP_201_CREATED, headers=headers)

class KidCreateView(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = KidSerializer
    permission_classes = [IsAuthenticatedParent]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        kid = CustomUser.objects.create_user(
            username=data['username'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            personal_id=data['personal_id'],
            parent=request.user  # Assign the parent field
        )
        kid.save()
        return Response({"message": "Kid account created successfully"}, status=status.HTTP_201_CREATED)

class ParentWithKidsView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ParentWithKidsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ParentLoginView(GenericAPIView):
    serializer_class = ParentLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

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
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_parent:
            login(request, user)
            return Response({"message": "Successfully logged in"}, status=200)

        return Response({"error": "Invalid credentials"}, status=400)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Successfully logged out"}, status=200)
