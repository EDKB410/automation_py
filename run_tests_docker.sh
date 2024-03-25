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

name=opencart
ip=$(grep ${name} /etc/hosts| cut -f1)

docker run \
	--rm \
	--add-host ${name}:${ip} \
	-v "/home/user/otus-qa-selenium/artifacts/:/app/artifacts" \
	--name tests tests \
	--executor=${name} \
	--base-url=http://${name}:8081 \
	--myip=${name} \
	--headless \
	--alluredir=artifacts/allure-results \
	$@
