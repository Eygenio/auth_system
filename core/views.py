from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.utils import timezone

from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    RoleSerializer, PermissionSerializer, UserRoleSerializer, RolePermissionSerializer
)
from .permissions import HasPermission, IsAdminUser


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'Пользователь успешно зарегистрирован',
            'user_id': str(user.id)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        user.last_login = timezone.now()
        user.save()

        return Response({
            'message': 'Вход выполнен успешно',
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Выход выполнен успешно'})


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Мягкое удаление
        request.user.is_active = False
        request.user.deleted_at = timezone.now()
        request.user.save()
        logout(request)
        return Response({'message': 'Аккаунт успешно удален'})


# Административные endpoints
class RoleListView(generics.ListCreateAPIView):
    from .models import Role
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    permission_required = 'role.manage'


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    from .models import Role
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    permission_required = 'role.manage'


class PermissionListView(generics.ListCreateAPIView):
    from .models import Permission
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    permission_required = 'permission.manage'


class UserRoleListView(generics.ListCreateAPIView):
    from .models import UserRole
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    permission_required = 'user_role.manage'


class RolePermissionListView(generics.ListCreateAPIView):
    from .models import RolePermission
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    permission_required = 'role_permission.manage'
