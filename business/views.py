from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from core.permissions import HasPermission

# Mock данные для демонстрации
PROJECTS = [
    {'id': 1, 'name': 'Проект А', 'owner': 'user1@example.com'},
    {'id': 2, 'name': 'Проект Б', 'owner': 'user2@example.com'},
    {'id': 3, 'name': 'Проект В', 'owner': 'admin@example.com'},
]

TASKS = [
    {'id': 1, 'project_id': 1, 'title': 'Задача 1', 'assigned_to': 'user1@example.com'},
    {'id': 2, 'project_id': 1, 'title': 'Задача 2', 'assigned_to': 'user2@example.com'},
    {'id': 3, 'project_id': 2, 'title': 'Задача 3', 'assigned_to': 'admin@example.com'},
]

@api_view(['GET'])
@permission_classes([HasPermission])
def project_list(request):
    """Список проектов - требуется permission: project.view"""
    return Response(PROJECTS)

@api_view(['GET'])
@permission_classes([HasPermission])
def project_detail(request, project_id):
    """Детали проекта - требуется permission: project.view"""
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if not project:
        return Response({'error': 'Проект не найден'}, status=status.HTTP_404_NOT_FOUND)
    return Response(project)

@api_view(['POST'])
@permission_classes([HasPermission])
def project_create(request):
    """Создание проекта - требуется permission: project.create"""
    new_project = {
        'id': len(PROJECTS) + 1,
        'name': request.data.get('name'),
        'owner': request.user.email
    }
    PROJECTS.append(new_project)
    return Response(new_project, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([HasPermission])
def task_list(request):
    """Список задач - требуется permission: task.view"""
    return Response(TASKS)

@api_view(['POST'])
@permission_classes([HasPermission])
def task_create(request):
    """Создание задачи - требуется permission: task.create"""
    new_task = {
        'id': len(TASKS) + 1,
        'project_id': request.data.get('project_id'),
        'title': request.data.get('title'),
        'assigned_to': request.data.get('assigned_to', request.user.email)
    }
    TASKS.append(new_task)
    return Response(new_task, status=status.HTTP_201_CREATED)
