from django.db import transaction


def create_default_permissions():
    """Создание стандартных разрешений"""
    from .models import Permission

    permissions_data = [
        {'name': 'Просмотр проектов', 'code': 'project.view'},
        {'name': 'Создание проектов', 'code': 'project.create'},
        {'name': 'Редактирование проектов', 'code': 'project.edit'},
        {'name': 'Удаление проектов', 'code': 'project.delete'},
        {'name': 'Просмотр задач', 'code': 'task.view'},
        {'name': 'Создание задач', 'code': 'task.create'},
        {'name': 'Редактирование задач', 'code': 'task.edit'},
        {'name': 'Удаление задач', 'code': 'task.delete'},
        {'name': 'Управление ролями', 'code': 'role.manage'},
        {'name': 'Управление разрешениями', 'code': 'permission.manage'},
        {'name': 'Управление ролями пользователей', 'code': 'user_role.manage'},
        {'name': 'Управление разрешениями ролей', 'code': 'role_permission.manage'},
    ]

    for data in permissions_data:
        Permission.objects.get_or_create(**data)


def create_default_roles():
    """Создание стандартных ролей"""
    from .models import Role

    roles_data = [
        {'name': 'Администратор', 'description': 'Полный доступ ко всем функциям'},
        {'name': 'Менеджер', 'description': 'Управление проектами и задачами'},
        {'name': 'Разработчик', 'description': 'Работа с задачами'},
        {'name': 'Гость', 'description': 'Ограниченный доступ'},
    ]

    for data in roles_data:
        Role.objects.get_or_create(**data)


def assign_permissions_to_roles():
    """Назначение разрешений ролям"""
    from .models import Role, Permission, RolePermission

    admin_role = Role.objects.get(name='Администратор')
    manager_role = Role.objects.get(name='Менеджер')
    developer_role = Role.objects.get(name='Разработчик')
    guest_role = Role.objects.get(name='Гость')

    # Все разрешения для администратора
    all_permissions = Permission.objects.all()
    for permission in all_permissions:
        RolePermission.objects.get_or_create(role=admin_role, permission=permission)

    # Разрешения для менеджера
    manager_permissions = Permission.objects.filter(
        code__in=['project.view', 'project.create', 'project.edit',
                  'task.view', 'task.create', 'task.edit']
    )
    for permission in manager_permissions:
        RolePermission.objects.get_or_create(role=manager_role, permission=permission)

    # Разрешения для разработчика
    developer_permissions = Permission.objects.filter(
        code__in=['project.view', 'task.view', 'task.edit']
    )
    for permission in developer_permissions:
        RolePermission.objects.get_or_create(role=developer_role, permission=permission)

    # Разрешения для гостя
    guest_permissions = Permission.objects.filter(code='project.view')
    for permission in guest_permissions:
        RolePermission.objects.get_or_create(role=guest_role, permission=permission)
