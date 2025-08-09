#!/usr/bin/env bash

set -e

code_home=${0%/*}

venv=${code_home}/../.venv

. ${venv}/bin/activate

python ${code_home}/../app.py