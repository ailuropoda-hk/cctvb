FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && apt-add-repository --yes --update ppa:ansible/ansible && apt-get install -y ansible python-pip vim jq
RUN apt-get install -y sshpass iputils-ping

RUN pip install --no-cache-dir passlib
RUN pip install --no-cache-dir pycrypto

RUN echo "#!/bin/sh" >> /usr/local/bin/docker-entrypoint.sh
RUN echo "set -e" >> /usr/local/bin/docker-entrypoint.sh
RUN echo "exec $@" >> /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /app/ansible

CMD ["docker-entrypoint.sh"]