FROM pytorch/pytorch:latest
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99

RUN mkdir -p /usr/share/man/man1

RUN apt update
# RUN apt install default-jdk scala git -y
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get -y install vim

# Install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["python","main.py"]
