import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django')


class LogMiddle(MiddlewareMixin):
    def process_request(self, request):
        # 存放请求过来时的时间
        request.init_time = time.time()
        # 请求路径
        path = request.path
        user = request.user
        method = request.method
        logger.info("request path: {}".format(path))
        logger.info("request method: {}".format(method))
        if user:
            logger.info("request user: {}-{}".format(user.id, user.username))
        return None

    def process_response(self, request, response):
        # 耗时
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        e_time = time.time() - request.init_time
        # 请求路径
        path = request.path
        # 请求方式
        method = request.method
        # 响应状态码
        status_code = response.status_code
        logger.info('%s %s %s %s' % (localtime, path, method, status_code))
        logger.info('Elapsed Time: %s ms' % (e_time * 1000))
        return response

    def process_exception(self, request, exception):
        logging.error(exception)
