FROM rabbitmq:4.0.0-rc.1-management-alpine

USER root

RUN apk add --no-cache gettext
COPY conf/rabbitmq.conf.template /etc/rabbitmq/rabbitmq.conf.template
COPY conf/definitions.json.template /etc/rabbitmq/definitions.json.template

# Добавляем скрипт для замены переменных окружения в шаблоне конфигурации
COPY /init_rabbitmq.sh /init_rabbitmq.sh
RUN chmod +x /init_rabbitmq.sh
CMD ["/init_rabbitmq.sh"]