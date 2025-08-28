#!/usr/bin/env python
import os
import sys

# Добавляем текущую директорию в Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import execute_from_command_line

execute_from_command_line(['manage.py', 'makemigrations', 'core'])
execute_from_command_line(['manage.py', 'makemigrations', 'business'])
execute_from_command_line(['manage.py', 'migrate'])