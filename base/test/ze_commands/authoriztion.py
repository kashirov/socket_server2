# coding: utf8

from base.test.ze_commands.base_command import BaseCommand
import hashlib

class Authorization(BaseCommand):

    name = 'user.authorization'
    params = 'uid', 'auth_key'

    def execute(self, uid, auth_key):

        if self.checkSig(uid, auth_key):
            self.client.login(uid)
        else:
            self.msg.result = 2
            self.msg.text = 'bad auth_key'

        return self.msg


    def checkSig(self, uid, auth_key):

        app_id = 609145
        app_key = '196d36afd567170464a7bcef1e6d3789'

        sig = hashlib.md5(str(app_id) + '_' + uid + '_' + app_key).hexdigest()

        if sig == auth_key:
            return True
        else:
            return False
