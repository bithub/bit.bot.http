from OpenSSL import SSL

from zope.component import getUtility

from twisted.web import server

from bit.core.interfaces import IConfiguration
from bit.bot.http.interfaces import IHTTPRoot


def getHTTPSPort():
    return int(getUtility(IConfiguration).get('https', 'port') or 0)


def getHTTPSSite():
    return server.Site(getUtility(IHTTPRoot))


class SSLContextFactory(object):
    def getContext(self):
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        cert = getUtility(IConfiguration).get('https', 'cert')
        key = getUtility(IConfiguration).get('https', 'key')
        if cert and key:
            ctx.use_certificate_file(cert)
            ctx.use_privatekey_file(key)
            return ctx
