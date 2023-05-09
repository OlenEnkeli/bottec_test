#!/bin/bash

poetry run uvicorn --reload app.api:app --port 8000 --timeout-keep-alive 10000 --env-file .env
