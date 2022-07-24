import json
import logging

from websocket import create_connection

from deer_block.settings import WS_URL

logger = logging.getLogger(__name__)


class ConnectWebsocket:
    def __init__(self, user_id, route):
        self.url = '{ws_url}ws/system/{route}/{user_id}/'.format(ws_url=WS_URL, route=route, user_id=user_id)
        self.ws = None

    def get_connect(self):
        ws = create_connection(self.url)
        if ws.getstatus() != 101:
            logger.error("链接{}未能连接成功.".format(self.url))
            return None
        self.ws = ws
        logger.info("websocket连接打开，链接为：{}，状态是：{}".format(self.url, ws.getstatus()))
        return ws

    def send_message(self, message: dict):
        self.ws.send(json.dumps(message, ensure_ascii=False))

    def close_connect(self):
        self.ws.close()
        logger.info("websocket连接关闭")
