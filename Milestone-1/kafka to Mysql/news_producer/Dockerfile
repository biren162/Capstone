FROM ubuntu:18.04
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get -y install vim sudo
COPY ./news_producer.py ./
COPY ./requirements.txt ./
RUN sudo apt update
RUN sudo apt install software-properties-common -y
RUN sudo apt-get install python3.7 -y

RUN set -xe \
    && apt-get update -y \
    && apt-get install python3-pip -y
RUN sudo apt-get install python3-dev
RUN sudo pip3 install --upgrade setuptools
RUN sudo pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt
ADD ./data/. /data/
CMD ["news_producer.py"]
ENTRYPOINT ["python3"]

