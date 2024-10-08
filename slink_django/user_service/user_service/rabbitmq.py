import pika
import json
from django.conf import settings

def send_message(queue, message, response_queue):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,  # Проверьте здесь правильность хоста
            port=int(settings.RABBITMQ_PORT),
            virtual_host=settings.RABBITMQ_VHOST,  # Убедитесь, что порт числовой
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue, durable=True)
    channel.queue_declare(response_queue, durable=True)

    message['response_queue'] = response_queue
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2  # Make message persistent
        )
    )
    connection.close()

def receive_message(queue):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,  # Проверьте здесь правильность хоста
            port=int(settings.RABBITMQ_PORT),
            virtual_host=settings.RABBITMQ_SERVICES_VHOST,  # Убедитесь, что порт числовой
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue, durable=True)

    method_frame, header_frame, body = channel.basic_get(queue)
    if method_frame:
        message = json.loads(body)
        channel.basic_ack(method_frame.delivery_tag)
        connection.close()
        return message
    connection.close()
    return {'status': 'error', 'message': 'Нет ответа'}

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received response: {message}")


def start_consuming(queue_name):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,  # Проверьте здесь правильность хоста
            port=int(settings.RABBITMQ_PORT),
            virtual_host=settings.RABBITMQ_SERVICES_VHOST,  # Убедитесь, что порт числовой
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Waiting for messages in {queue_name}...")
    channel.start_consuming()