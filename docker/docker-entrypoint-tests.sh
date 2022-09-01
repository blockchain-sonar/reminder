#!/bin/sh

source /usr/local/blockchain-sonar/reminder/backend/.venv/bin/activate

export PYTHONPATH=/usr/local/blockchain-sonar/reminder/backend

python -m xmlrunner discover --output-file /data/test-results.xml -v
