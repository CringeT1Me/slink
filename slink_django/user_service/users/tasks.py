import uuid

from user_service.celery import app

from user_service.rabbitmq import send_message, receive_message

@app.task
def send_friend_request(user_id, friend_id):
    queue = 'send_friend_request_queue'
    message = {
        'action': 'send_friend_request',
        'user_id': user_id,
        'friend_id': friend_id,
    }
    response_queue_name = 'send_friend_request_response_queue'
    response_queue = response_queue_name + str(uuid.uuid4())
    send_message(queue, message, response_queue)
    return receive_message(response_queue)

@app.task
def create_albums(user_id):
    queue = 'create_albums_queue'
    message = {
        'action': 'create_albums',
        'user_id': user_id,
    }
    response_queue_name = 'create_albums_response_queue'
    response_queue = response_queue_name + str(uuid.uuid4())
    send_message(queue, message, response_queue)
    return receive_message(response_queue)


def cancel_friend_request(user_id, friend_id):
    queue = 'cancel_friend_request_queue'
    message = {
        'action': 'send_friend_request',
        'user_id': user_id,
        'friend_id': friend_id,
    }
    response_queue_name = 'cancel_friend_request_response_queue'
    response_queue = response_queue_name + str(uuid.uuid4())
    send_message(queue, message, response_queue)
    return receive_message(response_queue)