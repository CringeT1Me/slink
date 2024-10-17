import logging

from django.core.management.base import BaseCommand
from rabbitmq.rabbitmq import start_consuming
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start RabbitMQ consumer'

    def handle(self, *args, **kwargs):
        logger.info('hello')

        queues = ['create_albums_queue']
        print("Start consuming...")
        start_consuming(queues)
        print("End consuming...")