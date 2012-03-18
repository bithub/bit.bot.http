
from OpenSSL import SSL

from zope.component import getUtility
from twisted.web import server

from bit.core.interfaces import IConfiguration
from bit.bot.common.interfaces import IHTTPRoot

def getHTTPSPort():
    return int(getUtility(IConfiguration).get('https','port'))

def getHTTPSSite():
    return server.Site(getUtility(IHTTPRoot))

class SSLContextFactory(object):
    def getContext(self):
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_certificate_file(getUtility(IConfiguration).get('https','cert'))
        ctx.use_privatekey_file(getUtility(IConfiguration).get('https','key'))
        return ctx

def getWSSPort():
    return int(getUtility(IConfiguration).get('wss','port'))
    
def getFlashPolicyPort():
    return 8043
#return int(getUtility(IConfiguration).get('wss','port'))
