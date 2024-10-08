from friendship.models import Friendship


def handle_request(message):
    if message['action'] == 'send_friend_request':
        user_id = message['user_id']
        friend_id = message['friend_id']
        # Логика добавления запроса на дружбу
        return Friendship.add_friend_request(user_id, friend_id)

    elif message['action'] == 'cancel_friend_request':
        user_id = message['user_id']
        friend_id = message['friend_id']
        # Логика добавления запроса на дружбу
        return Friendship.delete_friend_request(user_id, friend_id)
