import http
import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler

from exceptions.custom_errors import CustomError

logger = logging.getLogger('django')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    logger.error("发生异常：\nexc: {}\ncontext: {}".format(str(exc), str(context)))
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['code'] = -1
        if isinstance(exc, CustomError):
            error_dict = exc.to_serializer()
            response.data.update(error_dict)
        else:
            response.data["message"] = str(exc)
    else:
        response = Response(
            data={"status_code": http.HTTPStatus.INTERNAL_SERVER_ERROR, "code": -1, "message": str(exc)},
            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)
    return response
