import datetime

from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from apps.bussiness.models import TaskLog
from apps.celerytask.base_task import BaseTask
from apps.square.models import Issues
from apps.users.models import User
from deer_block import celery_app
from utils.send_message.connect_ws import ConnectWebsocket

logger = get_task_logger(__name__)


@celery_app.task(bind=True, base=BaseTask, name="send_issues_message", max_retries=3, serializer='json',
                 default_retry_delay=20)
def send_issues_message(self, user_id, issues_id, *args, **kwargs):
    try:
        ws_client = ConnectWebsocket(user_id, route="issues")
        ws_client.get_connect()
    except Exception as e:
        logger.error("Websocket连接错误...")
        raise self.retry(exc=e)
    user = User.logic_objects.filter(id=user_id).first()
    issues = Issues.logic_objects.filter(id=issues_id).first()
    try:
        tl = TaskLog.logic_objects.filter(celery_task_id=self.request.id).first()
        if not tl:
            tl = TaskLog.init_entity(self.request.id, self.name, kwargs)
        tl.login = user
        tl.from_model = "issues"
        res = AsyncResult(self.request.id)
        tl.final_status = res.status
        tl.save()
    except Exception as e:
        logger.error("task log 保存失败....")
        raise self.retry(exc=e)
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
    try:
        ws_client.send_message(message)
        logger.info(
            " {username} 新发布的动态 {issues_name} ，消息发送至websocket".format(username=user.username, issues_name=issues.title))
        ws_client.close_connect()
    except Exception as e:
        logger.error("websocket发送失败或是关闭websocket资源失败...")
        raise self.retry(exc=e)
