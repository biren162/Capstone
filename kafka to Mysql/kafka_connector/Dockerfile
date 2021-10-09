FROM ubuntu:18.04
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt install curl -y
COPY ./entrypoint.sh ./
RUN chmod +x /entrypoint.sh
entrypoint ["/entrypoint.sh"]
