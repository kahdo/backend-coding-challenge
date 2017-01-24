#!/bin/bash
celery -A hello worker --loglevel=info
