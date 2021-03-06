# coding: utf8

from socket_server.base.common import Common, client_try
from socket_server.base.packer import Packer
import select


class BaseClient(Common, Packer):

    count = 0

    def __init__(self, sock, addr, talker):
        self.id = self.__get_id()

        self.sock = sock
        self.talker = talker
        self.poll = talker.epoll

        self.fileno = sock.fileno()
        self.queue = []
        self.peername = addr

        self.request = b''
        self.response = b''
        self.size = None

    def __get_id(self):
        BaseClient.count += 1
        return self.count

    @client_try
    def recv(self):
        data = self.sock.recv(self.size or 4)
        if not data:
            self.unregister()
        else:
            if not self.size:
                self.size = self.packsize(data)
            else:
                self.request += data
                if len(self.request) >= self.size:
                    self.listen(self.unpack(self.size, self.request[:self.size]))
                    self.request = b''
                    self.size = None

    def listen(self, request):
        ''' What to do with request? '''

    def add_resp(self, resp):
        self.queue.insert(0, resp)
        self.refresh_state()

    def send(self):
        written = self.sock.send(self.response)
        self.response = self.response[written:]

    @client_try
    def reply(self):
        if not self.response:
            self.response = self.encode(self.queue.pop())

        self.send()

        if not self.response:
            self.response = b''
            self.refresh_state()

    def unregister(self):
        self.talker.unregister(self.fileno)

    def close(self):
        self.sock.close()
        self.disconnect(self.id)

    @property
    def has_reponse(self):
        return len(self.queue) > 0

    def modify(self, etype):
        try:
            self.poll.modify(self.fileno, etype)
        except:
            self.unregister()

    def refresh_state(self, etype=None):
        etype = select.EPOLLOUT if self.has_reponse else select.EPOLLIN
        self.modify(etype)
