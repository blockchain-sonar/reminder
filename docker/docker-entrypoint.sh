#!/bin/sh

source /usr/local/blockchain-sonar/reminder/backend/.venv/bin/activate

export PYTHONPATH=/usr/local/blockchain-sonar/reminder/backend

export FLASK_APP=blockchain_sonar_reminder_backend
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
export FLASK_ENV=development
export FLASK_DEBUG=0

exec python -m flask run
