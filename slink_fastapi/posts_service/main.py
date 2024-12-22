import logging
import uvicorn
from api.v1.routes import router as router_v1
from core.config import settings
from core.fastapi_app import create_app


logging.basicConfig(
    format=settings.logging.log_format,
)

app = create_app(
    create_custom_static_urls=True,
)

app.include_router(router_v1, prefix=settings.api_v1_prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
