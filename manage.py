#!/usr/bin/env python
"""Утилита командной строки Django для административных задач."""
import os
import sys


def main():
    """Запуск административных задач."""
    # Устанавливаем переменную окружения для настроек Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    try:
        # Пытаемся импортировать Django management утилиты
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Обработка ошибки если Django не установлен
        raise ImportError(
            "Не удалось импортировать Django. Вы уверены что он установлен и "
            "доступен через переменную окружения PYTHONPATH? Не забыли ли вы "
            "активировать виртуальное окружение?"
        ) from exc

    # Выполняем команду из командной строки
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Запускаем main функцию при прямом вызове файла
    main()
