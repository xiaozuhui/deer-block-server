import datetime

from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from apps.business.models import Comment, TaskLog
from apps.celerytask.base_task import BaseTask
from apps.consts import SourceType
from apps.square.models import Issues
from apps.users.models import User
from deer_block import celery_app
from utils.send_message.connect_ws import ConnectWebsocket

logger = get_task_logger(__name__)


@celery_app.task(bind=True, base=BaseTask, name="send_thumbsub_message", max_retries=3, serializer='json',
                 default_retry_delay=20)
def send_thumbsub_message(self, user_id, issues_id, comment_id=None, *args, **kwargs):
    """对issues或是comment进行点赞的通知
    """
    user = User.logic_objects.filter(id=user_id).first()
    issues = Issues.logic_objects.filter(id=issues_id).first()
    if not user or not issues:
        raise ValueError("user[{}] or issues[{}] 不存在".format(user_id, issues_id))
    to_user = issues.publisher
    message = {
        "from_user_id": user.id,
        "to_user_id": to_user.id,
        "callback": "system_message",  # 这个回调函数是用来发送到websocket的
        "send_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "issues_title": issues.title,
        "issues_id": issues.id,
        "issues_url": r'/square/issues/{id}/'.format(id=issues_id),  # 对应的issues链接
    }
    try:
        tl = TaskLog.logic_objects.filter(celery_task_id=self.request.id).first()
        if not tl:
            tl = TaskLog.init_entity(self.request.id, self.name, kwargs)
        tl.login = user
        tl.from_model = SourceType.THUMB_UP
        res = AsyncResult(self.request.id)
        tl.final_status = res.status
        tl.save()
    except Exception as e:
        logger.error("task log 保存失败....")
        raise self.retry(exc=e)

    log_str = f"{user.username} 对评论 {issues.title} 进行了点赞，消息发送至websocket"
    if comment_id:
        comment = Comment.logic_objects.filter(id=comment_id).first()
        if not comment:
            raise ValueError("Comment[{}]不存在".format(comment_id))
        message.update({
            "comment_id": comment.id,
            "comment_url": r"/business/comment/{id}/".format(id=comment_id),
        })
        log_str = f"{user.username} 对评论 {comment_id} 进行了点赞，消息发送至websocket"
    try:
        ws_client = ConnectWebsocket(to_user.id, route="thumbsup")
        ws_client.get_connect()
        ws_client.send_message(message)
        logger.info(log_str)
        ws_client.close_connect()
    except Exception as e:
        raise self.retry(exc=e)
