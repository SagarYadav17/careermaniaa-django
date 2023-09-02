#!/bin/bash

# Start Celery Workers
celery -A config worker -l info &> ./celery.log &

gunicorn 'config.wsgi' --bind=0.0.0.0:8000
