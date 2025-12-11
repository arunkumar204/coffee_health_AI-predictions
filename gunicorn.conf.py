# gunicorn.conf.py
import multiprocessing

# Gunicorn config for Render memory optimization
bind = "0.0.0.0:10000"
workers = 1  # Only 1 worker to save memory
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
