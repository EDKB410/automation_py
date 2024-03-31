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

export UID

export GID=$(id -u)

rm -rf artifacts

mkdir -p artifacts

docker network create --driver bridge test_net || true

export PYTEST_ARGS="$@"

docker-compose up --abort-on-container-exit

tests_status=$?

docker-compose down

docker network rm test_net

exit ${tests_status}
