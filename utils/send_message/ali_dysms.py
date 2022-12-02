from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
from alibabacloud_tea_openapi import models as open_api_models

from deer_block.settings import ALI_SEND_CONFIG, SEND_MESSAGE_ACCESS_KEY, SEND_MESSAGE_ACCESS_SECRET


class AliDysms:
    def __init__(self, mod="ral"):
        self.client = AliDysms._client(SEND_MESSAGE_ACCESS_KEY, SEND_MESSAGE_ACCESS_SECRET)
        self.mod = mod

    @staticmethod
    def _parse_sms_config(mod):
        """解析发送模版，从setting中获取
        """
        mod = ALI_SEND_CONFIG.get(mod, None)
        if not mod:
            raise Exception("请在设置中正确配置发送签名和模版编码")
        sign_name = mod.get("sign_name")
        template_code = mod.get("template_code")
        return sign_name, template_code

    @staticmethod
    def _client(access_key_id, access_key_secret):
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return DysmsapiClient(config)

    def send_message(self, phone_number: str, code: str) -> dict:
        """发送短信

        Args:
            phone_number (str): 手机号
            code (str): 验证码
        Return: 
            body: {
                "RequestId": "3ABDDAA3-4BE3-53A2-AA64-783B0256F23B",
                "Message": "OK",
                "BizId": "549608351597292246^0",
                "Code": "OK"
            }
        """
        if not phone_number:
            raise ValueError("手机号为必填")
        if not code:
            raise ValueError("验证码为必填")
        sign_name, template_code = AliDysms._parse_sms_config(self.mod)
        send_sms_request = dysmsapi_models.SendSmsRequest(
            sign_name=sign_name,
            template_code=template_code,
            phone_numbers=phone_number,
            template_param='{"code": "' + code + '"}'
        )
        # 复制代码运行请自行打印 API 的返回值
        res = self.client.send_sms(send_sms_request)
        return res.body.to_map()
