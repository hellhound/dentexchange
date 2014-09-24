# -*- coding:utf-8 -*-
import unittest

from libs.singleton import Singleton


class SingletonTestCase(unittest.TestCase):
    class SingletonClass(object):
        __metaclass__ = Singleton

    def test_call_should_return_same_instance(self):
        # setup
       obj1 = self.SingletonClass()

       # action
       obj2 = self.SingletonClass()

       # assert
       self.assertEqual(id(obj1), id(obj2))
