from django.test import TestCase

from exceptions.custom_excptions.business_error import BusinessError


class CustomErrorTest(TestCase):
    def test_business_error(self):
        # 检查两种不同的形式是否一致
        err1 = BusinessError('ErrNoThumbUp')
        err2 = BusinessError.ErrNoThumbUp
        self.assertEqual(err1, err2)
