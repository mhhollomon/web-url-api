#!/usr/bin/env bash

set -e

code_home=${0%/*}

venv=${code_home}/../.venv

. ${venv}/bin/activate

# switch groups before running so the
# unix socket has the correct group.
sg rproxy "python ${code_home}/../app.py"