#!/bin/sh

# Подставляем переменные окружения в файл конфигурации
envsubst < /usr/local/kong/declarative/kong.yml.template > /usr/local/kong/declarative/kong.yml

# Выполняем основную команду (запуск Kong)
exec "$@"


