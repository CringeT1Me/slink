FROM kong/kong-gateway:2.8-alpine

USER root

RUN apk add --no-cache gettext
COPY conf/kong.yml.template /usr/local/kong/declarative/kong.yml.template

# Добавляем скрипт для замены переменных окружения в шаблоне конфигурации
COPY /init_config.sh /init_config.sh
RUN chmod +x /init_config.sh

CMD ["/init_config.sh", "kong", "start", "--v"]

