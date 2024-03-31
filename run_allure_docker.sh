#!/bin/bash

usage()
{
    cat << USAGE >&2
Usage:
    ${0##*/} <allure command with options>
USAGE
    exit 1
}

if [ -z $1 ]; then
    usage
fi

PORT=${PORT:-8090}

docker run \
    --rm \
    --name allure \
    -p ${PORT}:${PORT} \
    --env PORT=${PORT} \
    --volume /home/user/otus-qa-selenium/artifacts/:/opt/artifacts/ \
    allure $@
