# coding: utf8

from client import Client
from handler import BaseHandler
from packer import Packer
import logging
import select


class Talker(BaseHandler, Packer):

    def register(self, sock, addr, type=select.POLLIN):
        self.clients[sock.fileno()] = Client(sock, addr, self)

        self.epoll_register(sock, type)
        logging.debug('register client %s' % len(self.clients))

    def process(self, client, event):
        if event & select.EPOLLIN:
            client.recv()
        elif event & select.EPOLLOUT:
            client.reply()
        elif event & select.EPOLLHUP or event & select.EPOLLERR:
            self.unregister(client.fileno)

    def stop(self):
        BaseHandler.stop(self)
        self.clients.subcriber.stop()