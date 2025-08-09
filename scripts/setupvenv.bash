#!/usr/bin/env bash

set -e

if [ ! -d ".venv" ]; then
  python -m venv .venv || exit
fi

. .venv/bin/activate

pip install -r requirements.txt