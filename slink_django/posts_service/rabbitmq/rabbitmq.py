import pika
import json
from django.conf import settings
from albums.tasks import create_albums
import logging

logger = logging.getLogger(__name__)

def handle_request(message):
    if message['action'] == 'create_albums':
        # Отправляем задачу на выполнение и возвращаем результат
        return create_albums.delay(message)

def send_message(channel, queue_name, message):
    try:
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2  # Делает сообщение устойчивым (persistent)
            )
        )
    except Exception as e:
        logger.error(f"Failed to send message to {queue_name}: {e}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    logger.info(f"Received message: {message}")
    try:
        result = handle_request(message)
        actual_result = result.get(timeout=60 * 15)  # Максимальное время ожидания ответа 15 минут
        logger.info(f"Result from Celery: {actual_result}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        actual_result = {'status': 'error', 'message': str(e)}

    # Отправляем результат обратно
    send_message(ch, message['response_queue'], actual_result)


def start_consuming(queues):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=int(settings.RABBITMQ_PORT),
            virtual_host=settings.RABBITMQ_SERVICES_VHOST,
            credentials=credentials
        )
    )
    channel = connection.channel()

    for queue in queues:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        print(f"Queue {queue} declared and consuming set up")  # Добавлено логирование перед стартом

    print("Starting consumer...")  # Лог перед началом потребления
    channel.start_consuming()

