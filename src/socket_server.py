# coding: utf8
from base.common import Common
from base.talker import Talker
from http.http_socket import HttpSocket
from threading import Thread
import os
import sys


class SocketServer(Thread):

    def __init__(self, name, config, mapper, auth_func, urls={}):
        Thread.__init__(self)

        self.mapper = mapper
        self.http_port = config.getint('sockets', 'http_port')
        self.talker = Talker(mapper,
                             port=config.getint('sockets', 'socket_port'),
                             db_channel=config.get('sockets', 'db_channel'))

        def named(s):
            return s % name

        def named_path(s):
            return os.path.abspath(named(s))

        Common.mapper = self.mapper

        if self.http_port:
            self.http_socket = HttpSocket(self.mapper, auth_func,
                                          self.http_port, urls=urls)
            self.http_socket.start()

    def run(self):
        self.talker.run()

    def stop(self, *q):
        if self.http_port:
            self.http_socket.stop()
        self.talker.stop()
        print 'socket is closed'
        sys.exit(0)