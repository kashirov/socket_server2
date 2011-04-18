# coding: utf8

from test.ze_mapper import Mapper

class Common(object):

    mapper = Mapper()
    policy_xml = '''<?xml version="1.0"?>
<!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy>
<allow-access-from domain="*" to-ports="*" secure="false" />
</cross-domain-policy>'''
