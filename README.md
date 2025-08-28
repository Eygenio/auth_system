# Система аутентификации и авторизации

## Архитектура системы

### Модели данных

1. **User** - пользователи системы
2. **Role** - роли пользователей
3. **Permission** - разрешения на действия
4. **UserRole** - связь пользователей с ролями
5. **RolePermission** - связь ролей с разрешениями

### Схема доступа

Пользователь → Роли → Разрешения → Доступ к ресурсам

### Стандартные роли и разрешения

1. **Администратор** - все разрешения
2. **Менеджер** - управление проектами и задачами
3. **Разработчик** - просмотр проектов, работа с задачами
4. **Гость** - только просмотр проектов

### API Endpoints

#### Аутентификация
- `POST /api/auth/register/` - регистрация
- `POST /api/auth/login/` - вход
- `POST /api/auth/logout/` - выход
- `GET/PUT/DELETE /api/auth/profile/` - управление профилем

#### Администрирование
- `GET/POST /api/admin/roles/` - управление ролями
- `GET/PUT/DELETE /api/admin/roles/{id}/` - управление конкретной ролью
- `GET/POST /api/admin/permissions/` - управление разрешениями
- `GET/POST /api/admin/user-roles/` - назначение ролей пользователям
- `GET/POST /api/admin/role-permissions/` - назначение разрешений ролям

#### Бизнес-объекты
- `GET /api/projects/` - список проектов (требует project.view)
- `GET /api/projects/{id}/` - детали проекта (требует project.view)
- `POST /api/projects/create/` - создание проекта (требует project.create)
- `GET /api/tasks/` - список задач (требует task.view)
- `POST /api/tasks/create/` - создание задачи (требует task.create)

### Настройка разрешений

Для защиты endpoint'а необходимо:
1. Добавить декоратор `@permission_classes([HasPermission])`
2. Указать требуемое разрешение в view: `permission_required = 'permission.code'`

### Обработка ошибок

- **401 Unauthorized** - пользователь не аутентифицирован
- **403 Forbidden** - у пользователя нет необходимых разрешений
