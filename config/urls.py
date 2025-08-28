from django.urls import path, include
from core.views import (
    register_view, login_view, logout_view, user_profile_view,
    RoleListView, RoleDetailView, PermissionListView,
    UserRoleListView, RolePermissionListView
)
from business.views import project_list, project_detail, project_create, task_list, task_create

urlpatterns = [
    # Аутентификация
    path('api/auth/register/', register_view, name='register'),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/profile/', user_profile_view, name='profile'),

    # Администрирование
    path('api/admin/roles/', RoleListView.as_view(), name='role-list'),
    path('api/admin/roles/<uuid:pk>/', RoleDetailView.as_view(), name='role-detail'),
    path('api/admin/permissions/', PermissionListView.as_view(), name='permission-list'),
    path('api/admin/user-roles/', UserRoleListView.as_view(), name='user-role-list'),
    path('api/admin/role-permissions/', RolePermissionListView.as_view(), name='role-permission-list'),

    # Бизнес-объекты
    path('api/projects/', project_list, name='project-list'),
    path('api/projects/<int:project_id>/', project_detail, name='project-detail'),
    path('api/projects/create/', project_create, name='project-create'),
    path('api/tasks/', task_list, name='task-list'),
    path('api/tasks/create/', task_create, name='task-create'),
]
