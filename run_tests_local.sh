#!/bin/bash

usage()
{
    cat << USAGE >&2
Usage:
    ${0##*/} <path[s] to tests to be executed>
USAGE
    exit 1
}

if [ $# -eq 0 ]; then
    usage
fi

ENV_DIR=environment/opencart

pushd ${ENV_DIR}
./up.sh

popd

./wait-for-it.sh opencart:3306 -t 180 --strict -- ./wait-for-it.sh opencart:8080 -t 180 --strict -- \
	pytest --alluredir=artifacts/allure-results $@

pushd ${ENV_DIR}
./down.sh

popd

