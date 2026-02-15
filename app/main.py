import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.routers import (
    auth,
    categories,
    orders,
    products,
    recommendations,
    users,
    chat,              # websocket chat (eski)
    notifications,     # ✅ yangi
    chat_messages,     # ✅ yangi (REST chat + DB)
    product_feedback
)

settings = get_settings()

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.sentry_environment,
        traces_sample_rate=settings.sentry_traces_sample_rate,
    )

app = FastAPI(title="Afruza Collection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(recommendations.router)
app.include_router(chat.router)           # websocket
app.include_router(chat_messages.router) # ✅ REST chat
app.include_router(notifications.router) # ✅ notifications
app.include_router(product_feedback.router)


# Media static files
app.mount("/media", StaticFiles(directory="app/media"), name="media")

from fastapi import FastAPI
import os

# app = FastAPI()

@app.get("/deploy-check")
def deploy_check():
    return {"status": "ok"}

@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


if settings.sentry_dsn:
    app = SentryAsgiMiddleware(app)
