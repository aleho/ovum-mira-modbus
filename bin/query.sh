#!/usr/bin/env bash
set -e

.venv/bin/python scripts/query.py "${@}"
