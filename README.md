# deer-block-server

## 介绍
鹿街社区后端

- 广场社区
- 交易商城


## 软件架构

主要模块分为以下几个：
- users 用户模块
- media 媒体模块
- square 广场动态模块
- business 业务关系模块
- shop 商城模块


## 配置项
这个配置项是环境变量，主要是用于本地运行程序
可以根据自己的需要修改里面的配置
```
POSTGRES_NAME=deer_block
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123456
POSTGRES_HOST=localhost
POSTGRES_PORT=15432
CACHE_LOCATION_IP=localhost
CACHE_LOCATION_PORT=16379
SEND_MESSAGE_ACCESS_KEY=LTAI5tKqWQhoEfRhyJKc15yW
SEND_MESSAGE_ACCESS_SECRET=FGhlSPqkSE7qmZksPUYya762j2AdaR
SEND_MSG_MODE=aliyun
SIGN_NAME=阿里云短信测试
TEMPLATE_CODE=SMS_154950909
MINIO_IP=localhost
MINIO_PORT=19090
MINIO_SET_IP=localhost
MINIO_SET_PORT=19090
MINIO_STORAGE_ACCESS_KEY=root
MINIO_STORAGE_SECRET_KEY=1qazXDR%?
```

## 对于后续架构的思考

1. 架构的转变，将不再使用单体应用，而是使用微服务架构
2. 由业务驱动转为领域事件驱动
3. 部分拆分的没有权限控制的且数据量可能比较大的数据，将保存在nosql中，而不会使用InnoDB


## 技术支持
[![simpleui](https://img.shields.io/badge/developing%20with-Simpleui-2077ff.svg)](https://github.com/newpanjing/simpleui)