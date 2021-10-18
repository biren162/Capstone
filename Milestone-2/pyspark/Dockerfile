FROM ubuntu:18.04
#**************************************** INSTALLLING java ******************************
RUN apt-get -y update
RUN apt-get -y upgrade 
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get -y install openjdk-8-jdk
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH $PATH:/usr/lib/jvm/java-8-openjdk-amd64/bin
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >>~/.bash_profile
RUN echo "export PATH=$PATH:/usr/lib/jvm/java-8-openjdk-amd64/bin" >>~/.bash_profile

#**************************************** INSTALLING rsync vim sudo openssh-server ssh ******************************
RUN apt-get -y update
RUN apt-get -y upgrade 
RUN apt-get -y install rsync
RUN apt-get -y install vim sudo
RUN apt-get -y install openssh-server
RUN apt-get -y install ssh
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
RUN cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
RUN chmod 0600 ~/.ssh/authorized_keys
ADD ./config/ssh_config /etc/ssh/
EXPOSE 22
RUN echo "root:root" | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

#**************************************** INSTALLING spark and configure ******************************
RUN apt-get -y install scala
RUN mkdir spark
RUN wget -P /spark/ https://archive.apache.org/dist/spark/spark-2.3.2/spark-2.3.2-bin-hadoop2.7.tgz
RUN tar -xzvf /spark/spark-2.3.2-bin-hadoop2.7.tgz -C /spark
# ADD ./config/hive-site.xml ./spark/spark-2.3.2-bin-hadoop2.7/conf
ADD ./config/core-site.xml ./spark/spark-2.3.2-bin-hadoop2.7/conf
ADD ./config/hdfs-site.xml ./spark/spark-2.3.2-bin-hadoop2.7/conf
# ADD ./config/mapred-site.xml ./spark/spark-2.3.2-bin-hadoop2.7/conf
ENV SPARK_HOME /spark/spark-2.3.2-bin-hadoop2.7
ENV PATH $PATH:$SPARK_HOME/bin
ENV PYSPARK_PYTHON python3
RUN echo "export SPARK_HOME=/spark/spark-2.3.2-bin-hadoop2.7" >>~/.bash_profile
RUN echo "export PATH=$PATH:$SPARK_HOME/bin" >>~/.bash_profile
#RUN apt-get -y install python2.7 python-pip
RUN sudo apt update
RUN sudo apt install software-properties-common -y
#RUN sudo apt-get install --reinstall ca-certificates
#RUN sudo add-apt-repository ppa:deadsnakes/ppa -y
RUN sudo apt update
RUN sudo apt-get install python3.7 -y
RUN wget -P /spark/spark-2.3.2-bin-hadoop2.7/jars https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.8/spark-streaming-kafka-0-8-assembly_2.11-2.4.8.jar


#********************************************* Moving ~/.bash_profile to /etc/profile.d/ to get env variables to all users ****************
RUN cp ~/.bash_profile /etc/profile.d/bash_profile.sh
#**************************************** load script to start/stop the ecosystem ******************************
ADD ./config/start-mpp-ecosystem.sh .
ADD ./config/stop-mpp-ecosystem.sh .

ADD ./python/. /python/
COPY ./requirements.txt ./

#RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
#RUN sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 
#RUN sudo update-alternatives  --set python /usr/bin/python3.7
RUN sudo apt-get autoclean
RUN sudo apt-get autoremove
RUN sudo apt-get clean
RUN sudo apt-get update
RUN set -xe \
    && apt-get update -y \
    && apt-get install python3-pip -y
RUN sudo apt-get install python3-dev
RUN sudo pip3 install --upgrade setuptools
RUN sudo pip3 install --upgrade pip 
#RUN python3 -m pip install --upgrade pip
RUN pip3 install -r ./requirements.txt

EXPOSE 9092
EXPOSE 2181

