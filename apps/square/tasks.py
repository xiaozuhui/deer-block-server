import datetime
import json
import logging

from celery import shared_task
from websocket import create_connection

from apps.square.models import Issues
from apps.users.models import User
from deer_block.settings import WS_URL

logger = logging.getLogger('django')


@shared_task(bind=True)
def send_issues_message_2_websocket(self, user_id, issues_id, *args, **kwargs):
    url = '{ws_url}ws/system/issues/{user_id}/'.format(ws_url=WS_URL, user_id=user_id)
    ws = create_connection(url)
    if ws.getstatus() != 101:
        logger.error("链接{}未能连接成功.".format(url))
        return
    logger.info("websocket连接打开，链接为：{}，状态是：{}".format(url, ws.getstatus()))
    user = User.logic_objects.filter(id=user_id).first()
    issues = Issues.logic_objects.filter(id=issues_id).first()
    message = {
        "from_user": {
            "username": user.username,
            "user_id": user.id,
            "phone_number": user.phone_number,
        },
        "callback": "system_message",  # 这个回调函数是用来发送到websocket的
        "send_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "issues_title": issues.title,
        "content": issues.content if len(issues.content) < 25 else issues.content[:25] + "......",
        "issues_url": r'/square/issues/{id}/'.format(id=issues_id),  # 对应的issues链接
    }
    ws.send(json.dumps(message, ensure_ascii=False))
    logger.info(
        " {username} 新发布的动态 {issues_name} ，消息发送至websocket".format(username=user.username, issues_name=issues.title))
    ws.close()
    logger.info("websocket连接关闭")
