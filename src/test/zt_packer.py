# coding: utf8

from base.packer import Packer
from test import TestCase


class Zt_Packer(TestCase):

    def setUp(self):
        self.data = {'param1': 'param2', '1': 123, 'q': {'other': 'me'}}
        self.packer = Packer()

    def test_data(self):
        self.encoded = self.packer.encode(self.data)
        self.assertEqual(self.packer.decode(self.encoded), self.data)
