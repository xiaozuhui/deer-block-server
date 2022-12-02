import logging

from django_filters import rest_framework as rf
from rest_framework import filters
from rest_framework import status as status_
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

logger = logging.getLogger('django')


class JsonResponse(Response):
    """自定义Response
    """

    def __init__(self, data=None, code=0, msg="OK", status=200, headers=None, content_type=None):
        if data is None:
            data = {}
        logger.info("headers: {}\ncontent_type: {}\n".format(
            str(headers), str(content_type)))
        super(Response, self).__init__(None, status=status)
        self.data = {"code": code, "message": msg, "data": data}
        self.content_type = content_type
        self.headers = headers if headers else {}


class CustomViewBase(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (rf.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter,)
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'default': [IsAuthenticated]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # 没用明确权限的话使用默认权限
            return [permission() for permission in self.permission_classes_by_action['default']]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return JsonResponse(data=serializer.data, msg="OK", code=0, status=status_.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True,
                                             context={'user': request.user, "user_id": request.user.id})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True,
                                         context={'user': request.user, "user_id": request.user.id})
        return JsonResponse(data=serializer.data, code=0, msg="OK", status=status_.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'user': request.user, "user_id": request.user.id})
        return JsonResponse(data=serializer.data, code=0, msg="OK", status=status_.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial, context={'user': request.user, "user_id": request.user.id})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(data=serializer.data, msg="OK", code=0, status=status_.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data={}, code=0, msg="OK", status=status_.HTTP_204_NO_CONTENT)
