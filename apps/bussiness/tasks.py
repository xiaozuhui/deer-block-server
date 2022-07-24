import datetime
import logging

from celery import shared_task

from apps.bussiness.models import Comment
from apps.square.models import Issues
from apps.users.models import User
from utils.send_message.connect_ws import ConnectWebsocket

logger = logging.getLogger('django')


@shared_task(bind=True)
def send_comment_message_2_websocket(self, user_id, issues_id, comment_id, *args, **kwargs):
    user = User.logic_objects.filter(id=user_id).first()
    issues = Issues.logic_objects.filter(id=issues_id).first()
    comment = Comment.logic_objects.filter(id=comment_id).first()
    if not user or not issues or not comment:
        raise ValueError("user[{}] or issues[{}] or comment[{}] 不存在".format(user_id, issues_id, comment_id))
    to_user = issues.publisher
    # to_user是issues的user，但是当target_comment有值时，to_user将时target_comment的user
    target_comment_id = kwargs.get("target_comment_id", None)
    target_comment = None
    if target_comment_id:
        target_comment = Comment.logic_objects.filter(id=target_comment_id).first()
        to_user = target_comment.user
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
    ws_client = ConnectWebsocket(to_user.id, route="comment")
    ws_client.get_connect()
    ws_client.send_message(message)
    logger.info(
        " {username} 新发布的动态 {issues_name} ，消息发送至websocket".format(username=user.username, issues_name=issues.title))
    ws_client.close_connect()
