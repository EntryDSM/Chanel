#!/usr/bin/env bash

version='python -c "import chanel; print(chanel.__version__)"'

echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin registry.entrydsm.hs.kr

if [[ "$1" == "dev" ]];then
    echo "Docker build on dev started"

    docker build -t registry.entrydsm.hs.kr/chanel:dev .

    docker push registry.entrydsm.hs.kr/chanel:dev
elif [[ "$1" == "master" ]];then
    echo "Docker build on master started"

    docker build -t registry.entrydsm.hs.kr/chanel:${version} .

    docker tag registry.entrydsm.hs.kr/chanel:${version} registry.entrydsm.hs.kr/chanel:latest

    docker push registry.entrydsm.hs.kr/chanel:${version}
    docker push registry.entrydsm.hs.kr/chanel:latest

fi

exit
