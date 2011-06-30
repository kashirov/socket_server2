# coding: utf8

from base.common import trace
from base.packer import PackerDecodeError
from client import Client
from handler import BaseHandler
from packer import Packer
import logging
import select


class Talker(BaseHandler, Packer):

    port = 8885

    def register(self, sock, addr, type=select.POLLIN):
        self.clients[sock.fileno()] = Client(sock, addr, self.epoll)
        self.epoll_register(sock, type)
        logging.debug('register client %s' % len(self.clients))

    def recv(self, sock, size):
        try:
            data = sock.recv(size)
            if not data:
                self.unregister(sock.fileno())
            else:
                return data
        except Exception, s:
            trace()
            self.unregister(sock.fileno())


#    def login(self, client):
#        exist_client = self.clients.users.get(client.uid)
#        if exist_client:
#            self.unregister(exist_client.fileno)
#        self.clients.add_user(client)

    def process(self, client, event):
        logging.debug('talker clients %s' % len(self.clients))

        if event & select.EPOLLIN:
            data = self.recv(client.sock, 1024)
            if data:
                try:
                    data = self.decode(data)
                except PackerDecodeError, s:
                    client.logger.error('Decode Error %s' % s)
                else:
                    client.listen(data)
#                    if client.logged:
#                        self.login(client)

        elif event & select.EPOLLOUT:
            if client.has_reponse:
                client.reply()

