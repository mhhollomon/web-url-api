#!/usr/bin/env bash

set -e

code_home=${0%/*}

newgrp rproxy

venv=${code_home}/../.venv

. ${venv}/bin/activate

python ${code_home}/../app.py