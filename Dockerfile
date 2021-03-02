FROM ubuntu:18.04
MAINTAINER Martin Infante <maleinf09@gmail.com>
RUN apt-get update
RUN apt-get -y install gnupg wget
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - 
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" |  tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update
RUN apt-get install -y mongodb-org
RUN apt-get -y install python3-pip
RUN mkdir -p /usr/src/mongo_app/
WORKDIR /usr/src/mongo_app/
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
CMD ["/bin/bash", "init.sh"]
