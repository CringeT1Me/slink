#!/bin/sh

# Подставляем переменные окружения в файл конфигурации
envsubst < /etc/rabbitmq/definitions.json.template > /etc/rabbitmq/definitions.json
envsubst < /etc/rabbitmq/rabbitmq.conf.template > /etc/rabbitmq/rabbitmq.conf

# Запускаем RabbitMQ
exec rabbitmq-server