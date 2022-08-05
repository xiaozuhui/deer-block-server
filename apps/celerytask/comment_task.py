import datetime

from celery.result import AsyncResult
from celery.utils.log import get_task_logger

from apps.bussiness.models import Comment, TaskLog
from apps.celerytask.base_task import BaseTask
from apps.consts import SourceType
from apps.square.models import Issues
from apps.users.models import User
from deer_block import celery_app
from utils.send_message.connect_ws import ConnectWebsocket

logger = get_task_logger(__name__)


@celery_app.task(bind=True, base=BaseTask, name="send_comment_message", max_retries=3, serializer='json',
                 default_retry_delay=20)
def send_comment_message(self, user_id, issues_id, comment_id, *args, **kwargs):
    user = User.logic_objects.filter(id=user_id).first()
    issues = Issues.logic_objects.filter(id=issues_id).first()
    comment = Comment.logic_objects.filter(id=comment_id).first()
    if not user or not issues or not comment:
        raise ValueError("user[{}] or issues[{}] or comment[{}] 不存在".format(user_id, issues_id, comment_id))
    to_user = issues.publisher
    target_comment_id = kwargs.get("target_comment_id", None)
    target_comment = None
    if target_comment_id:
        target_comment = Comment.logic_objects.filter(id=target_comment_id).first()
        to_user = target_comment.user
    try:
        tl = TaskLog.logic_objects.filter(celery_task_id=self.request.id).first()
        if not tl:
            tl = TaskLog.init_entity(self.request.id, self.name, kwargs)
        tl.login = user
        tl.from_model = SourceType.COMMENT
        res = AsyncResult(self.request.id)
        tl.final_status = res.status
        tl.save()
    except Exception as e:
        logger.error("task log 保存失败....")
        raise self.retry(exc=e)
    message = {
        "from_user_id": user.id,
        "to_user_id": to_user.id,
        "callback": "system_message",  # 这个回调函数是用来发送到websocket的
        "send_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "issues_title": issues.title,
        "issues_id": issues.id,
        "comment_id": comment.id,
        "target_comment_id": target_comment_id,
        "content": comment.content if len(comment.content) < 25 else comment.content[:25] + "......",
        "issues_url": r'/square/issues/{id}/'.format(id=issues_id),  # 对应的issues链接
        "comment_url": r"/business/comment/{id}/".format(id=comment_id),
        "target_comment_url": r"/business/comment/{id}/".format(id=target_comment_id) if target_comment else "",
    }
    try:
        ws_client = ConnectWebsocket(to_user.id, route="comment")
        ws_client.get_connect()
        ws_client.send_message(message)
        if target_comment:
            logger.info('''{username} 对动态 {issues_name} 的评论 {comment_id} 进行了评论，
                        消息发送至websocket'''.format(username=user.username,
                                                 issues_name=issues.title,
                                                 comment_id=target_comment_id))
        else:
            logger.info('''{username} 对动态 {issues_name} 进行了评论，
                        消息发送至websocket'''.format(username=user.username,
                                                 issues_name=issues.title))

        ws_client.close_connect()
    except Exception as e:
        raise self.retry(exc=e)
