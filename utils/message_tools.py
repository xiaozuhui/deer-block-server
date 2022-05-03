# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_models

# 测试使用的短信服务，只有短信服务权限
# access_key_id： LTAI5tKqWQhoEfRhyJKc15yW
# access_key_secret： FGhlSPqkSE7qmZksPUYya762j2AdaR


def create_client(
    access_key_id: str,
    access_key_secret: str,
) -> DysmsapiClient:
    """
    使用AK&SK初始化账号Client
    @param access_key_id:
    @param access_key_secret:
    @return: Client
    @throws Exception
    """
    config = open_api_models.Config(
        # 您的AccessKey ID,
        access_key_id=access_key_id,
        # 您的AccessKey Secret,
        access_key_secret=access_key_secret
    )
    # 访问的域名
    config.endpoint = f'dysmsapi.aliyuncs.com'
    return DysmsapiClient(config)


def send_message(phone_number: str, code: str, access_key_id, access_key_secret):
    """发送短信

    Args:
        phone_number (_type_): 手机号
        code (_type_): 验证码
        access_key_id (_type_): _description_
        access_key_secret (_type_): _description_
    Return: 
        {
            "RequestId": "3ABDDAA3-4BE3-53A2-AA64-783B0256F23B",
            "Message": "OK",
            "BizId": "549608351597292246^0",
            "Code": "OK"
        }
    """
    client = create_client(access_key_id, access_key_secret)
    send_sms_request = dysmsapi_models.SendSmsRequest(
        sign_name='阿里云短信测试',
        template_code='SMS_154950909',
        phone_numbers=phone_number,
        template_param='{"code": "'+code+'"}'
    )
    # 复制代码运行请自行打印 API 的返回值
    res = client.send_sms(send_sms_request)
    return res.body.to_map()


# @staticmethod
# async def main_async(
#     args: List[str],
# ) -> None:
#     client = Sample.create_client('accessKeyId', 'accessKeySecret')
#     send_sms_request = dysmsapi_models.SendSmsRequest(
#         sign_name='阿里云短信测试',
#         template_code='SMS_154950909',
#         phone_numbers='17621753022',
#         template_param='{"code":"1234"}'
#     )
#     # 复制代码运行请自行打印 API 的返回值
#     await client.send_sms_async(send_sms_request)
