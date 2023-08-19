import time

from celery import shared_task


@shared_task
def send_code(code):
    print(code) # here should be a code sending to user phone number
    time.sleep(5)
    
