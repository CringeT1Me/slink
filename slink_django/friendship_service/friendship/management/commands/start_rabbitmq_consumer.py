from django.core.management.base import BaseCommand
from friendship.rabbitmq import start_consuming  # Подключаем вашу функцию

class Command(BaseCommand):
    help = 'Start RabbitMQ consumer'

    def handle(self, *args, **kwargs):
        queues = ['send_friend_request_queue', 'cancel_friend_request_queue']
        start_consuming(queues)