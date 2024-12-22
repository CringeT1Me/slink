from core.config import settings
from core.gunicorn import Application, get_app_options
from main import app


asgi_app = Application(
    application=app,
    options=get_app_options(
        host=settings.gunicorn.host,
        port=settings.gunicorn.port,
        timeout=settings.gunicorn.timeout,
        workers=settings.gunicorn.workers,
        log_level=settings.logging.log_level,
    ),
)


if __name__ == "__main__":
    asgi_app.run()
