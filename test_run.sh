#!/bin/bash

# 测试环境没有使用--port，这点需要在线上环境注意

docker build -t deer_block/deer-block-server:v1 .

docker run --name=deer_block_postgres -v /var/data/db:/var/lib/postgresql/data -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER=postgres -e POSTGRES_DB=deer_block -p 15432:5432 -itd postgres:13

docker run --name=deer_block_redis --net=bridge -p 16379:6379 -itd redis

docker run --name=deer_block_server -v /var/log/deer_block_server:/opt/deer_block/logs/ -e POSTGRES_NAME=deer_block -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=123456 -e OSS_ACCESS_KEY_ID=LTAI5tEqusWURSPxDZAWnhNZ -e OSS_ACCESS_KEY_SECRET=HRxY0tiNUCuQ553ku6Mxsma2ncdafn -e OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com -e OSS_BUCKET_NAME=papaw -e SEND_MESSAGE_ACCESS_KEY=LTAI5tKqWQhoEfRhyJKc15yW -e SEND_MESSAGE_ACCESS_SECRET=FGhlSPqkSE7qmZksPUYya762j2AdaR -e SEND_MSG_MODE=aliyun -e SIGN_NAME=阿里云短信测试 -e TEMPLATE_CODE=SMS_154950909 --link deer_block_redis:redis --link deer_block_postgres:db -p 18080:8088 -itd deer_block/deer-block-server:v1





