from celery import shared_task
import time
import random

@shared_task
def add(x, y):
    time.sleep(10)
    return x + y

@shared_task
def simulate_activity():
    """Generate random load for testing metrics."""
    for i in range(5):
        x, y = random.randint(1, 100), random.randint(1, 100)
        add.delay(x, y)
