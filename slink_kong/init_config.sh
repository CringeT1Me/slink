#!/bin/sh

envsubst < /usr/local/kong/declarative/kong.yml.template > /usr/local/kong/declarative/kong.yml

exec "$@"


