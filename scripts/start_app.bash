#!/usr/bin/env bash

set -e

code_home=${0%/*}

venv=${code_home}/../.venv

. ${venv}/bin/activate

env_path="${code_home}/../.env"

if [ -f $env_path ]; then
    . ${env_path}
else
    echo "No .env file found"
    exit 3
fi

if [ ! -z "${WAITRESS_LISTEN}" ]; then
    LISTEN_OPT="--listen=${WAITRESS_LISTEN}"
else
    LISTEN_OPT="--listen=localhost:5000"
fi

if [ ! -z "${WAITRESS_PREFIX}" ]; then
    PREFIX_OPT="--prefix=${WAITRESS_PREFIX}"
fi

waitress-serve --listen=${LISTEN_OPT} ${PREFIX_OPT} app.app