from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем настройки Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders.settings')

app = Celery('orders', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Загружаем настройки Celery из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(packages=['order'])

# Автоматически обнаруживаем задачи в приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
