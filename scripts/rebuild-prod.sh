#!/bin/bash
set -e

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

docker_file="${SCRIPTPATH}/../docker-compose.prod.yml"

git -C "${SCRIPTPATH}/.." pull origin master

docker-compose -f "$docker_file" up -d --build
