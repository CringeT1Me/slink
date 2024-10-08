import pika
import json
from django.conf import settings

from friendship.tasks import handle_request


def send_message(channel, queue_name, message):
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  # Делает сообщение устойчивым (persistent)
        )
    )

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received message: {message}")
    try:
        result = handle_request(message)
        print(result)
    except Exception as e:
        result = {'status': 'error', 'message': str(e)}
    send_message(ch, message['response_queue'], result)


def start_consuming(queues):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,  # Проверьте здесь правильность хоста
            port=int(settings.RABBITMQ_PORT),
            virtual_host=settings.RABBITMQ_SERVICES_VHOST,# Убедитесь, что порт числовой
            credentials=credentials
        )
    )
    channel = connection.channel()
    for queue in queues:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        print(f"Waiting for messages in {queue}...")
    channel.start_consuming()
