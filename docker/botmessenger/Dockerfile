FROM python:3.7

RUN apt-get update && \
    apt-get install -y \
    build-essential cmake libgtk-3-dev libboost-all-dev

RUN pip3 install --no-cache-dir numpy scipy scikit-image imutils matplotlib
RUN pip3 install --no-cache-dir opencv-python
RUN pip3 install --no-cache-dir pycrypto python-telegram-bot

RUN echo "#!/bin/sh" >> /usr/local/bin/docker-entrypoint.sh
RUN echo "set -e" >> /usr/local/bin/docker-entrypoint.sh
RUN echo "exec $@" >> /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /app/botmessenger

CMD ["docker-entrypoint.sh"]