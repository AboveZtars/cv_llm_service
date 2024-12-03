# gunicorn_config.py
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '3000')}"
backlog = 2048

# Worker processes
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'
worker_connections = 10
timeout = 30
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'