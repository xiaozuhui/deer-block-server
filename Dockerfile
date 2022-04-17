FROM ubuntu:20.04
ENV PYTHONUNBUFFERED=1
LABEL maintainer="xiaozuhui@outlook.com"
LABEL version="v1"
# 更新软件库
RUN  apt-get update --fix-missing
RUN  apt-get upgrade -y
# 安装 python3
RUN  apt-get install -y python3 python-dev python3-pip libpq-dev gunicorn postgresql-client
RUN mkdir -p /opt/deer_block
COPY . /opt/deer_block
WORKDIR /opt/deer_block
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple
# 将端口转发到8088
EXPOSE 8088