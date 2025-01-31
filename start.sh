#!/bin/bash
export DROP_TABLES=false
export ENV=dev
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info --no-access-log