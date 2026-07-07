#!/usr/bin/env python
import os
import sys
from django.core.management import call_command

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'birge.settings')
    
    # Автоматически применяем миграции при запуске
    call_command('migrate', interactive=False)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
