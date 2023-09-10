#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery -A src.tasks.tasks:cel worker --loglevel=INFO
elif [[ "${1}" == "flower" ]]; then
  celery -A src.tasks.tasks:cel flower
fi