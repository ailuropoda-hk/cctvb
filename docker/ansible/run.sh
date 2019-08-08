#!/bin/sh

cd ../../

docker build --rm -f ./docker/ansible/Dockerfile -t cctvb-ansible .
docker rm cctvb-ansible
docker run --name cctvb-ansible \
  -v $(pwd)/ansible/playbook:/app/ansible \
  -v $(pwd)/ansible/ansible.cfg:/etc/ansible/ansible.cfg  \
  -v $(pwd)/rpicam:/app/rpicam  \
  -v $(pwd)/keypair:/app/keypair \
  -it cctvb-ansible /bin/bash
