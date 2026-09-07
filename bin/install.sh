#!/usr/bin/env bash
set -e

python3 -m venv .venv
.venv/bin/pip install -e './[cli]'
