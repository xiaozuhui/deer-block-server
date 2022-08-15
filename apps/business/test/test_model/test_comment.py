import logging

from django.contrib.auth.hashers import make_password
from django.test import TestCase

from apps.square.models import Issues
from apps.users.models import User

logger = logging.getLogger('django.test')


class CollectionTest(TestCase):
    def setUp(self):
        """
        先初始化数据
        1、用户
        2、可收藏对象，这里将使用issues
        """
        logger.info("开始测试 Collection Model")
        logger.info("...创建 User")
        self.user = User.objects.create(id=1, username="user", email="user@example.com",
                                        password=make_password('123456'))
        logger.info("...创建 Issues")
        self.issues = Issues.objects.create(id=1, publisher=self.user, content="TestTest")

    def test_create_collection(self):
        """
        测试创建收藏
        """
        logger.info("测试 test_create_collection...")
        self.collection = self.issues.create_collect(self.user)
        self.assertEqual(self.issues.get_collect(self.user), self.collection)
