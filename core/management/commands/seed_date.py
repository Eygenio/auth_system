from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Заполнение базы данных тестовыми данными'

    def handle(self, *args, **options):
        # Импорты внутри функции
        from core.utils import create_default_permissions, create_default_roles, assign_permissions_to_roles
        from core.models import User, UserRole, Role

        try:
            with transaction.atomic():
                self.stdout.write('Создание разрешений...')
                create_default_permissions()

                self.stdout.write('Создание ролей...')
                create_default_roles()

                self.stdout.write('Назначение разрешений ролям...')
                assign_permissions_to_roles()

                # Создание тестовых пользователей
                self.stdout.write('Создание пользователей...')

                admin_user, created = User.objects.get_or_create(
                    email='admin@example.com',
                    defaults={
                        'first_name': 'Администратор',
                        'last_name': 'Системы',
                        'password': 'admin123',
                        'is_staff': True,
                        'is_superuser': True
                    }
                )
                if created:
                    admin_user.set_password('admin123')
                    admin_user.save()

                manager_user, created = User.objects.get_or_create(
                    email='manager@example.com',
                    defaults={
                        'first_name': 'Менеджер',
                        'last_name': 'Проектов',
                        'password': 'manager123'
                    }
                )
                if created:
                    manager_user.set_password('manager123')
                    manager_user.save()

                developer_user, created = User.objects.get_or_create(
                    email='developer@example.com',
                    defaults={
                        'first_name': 'Разработчик',
                        'last_name': 'Приложения',
                        'password': 'developer123'
                    }
                )
                if created:
                    developer_user.set_password('developer123')
                    developer_user.save()

                guest_user, created = User.objects.get_or_create(
                    email='guest@example.com',
                    defaults={
                        'first_name': 'Гость',
                        'last_name': 'Системы',
                        'password': 'guest123'
                    }
                )
                if created:
                    guest_user.set_password('guest123')
                    guest_user.save()

                # Назначение ролей
                admin_role = Role.objects.get(name='Администратор')
                manager_role = Role.objects.get(name='Менеджер')
                developer_role = Role.objects.get(name='Разработчик')
                guest_role = Role.objects.get(name='Гость')

                UserRole.objects.get_or_create(user=admin_user, role=admin_role)
                UserRole.objects.get_or_create(user=manager_user, role=manager_role)
                UserRole.objects.get_or_create(user=developer_user, role=developer_role)
                UserRole.objects.get_or_create(user=guest_user, role=guest_role)

                self.stdout.write(self.style.SUCCESS('Тестовые данные успешно созданы'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при создании тестовых данных: {str(e)}'))
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
