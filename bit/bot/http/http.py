from OpenSSL import SSL

from zope.component import getUtility

from twisted.web import server

from bit.core.interfaces import IConfiguration
from bit.bot.http.interfaces import IHTTPRoot


def getHTTPPort():
    return int(getUtility(IConfiguration).get('http', 'port') or 0)


def getHTTPSite():
    return server.Site(getUtility(IHTTPRoot))


def getWSPort():
    return int(getUtility(IConfiguration).get('ws', 'port') or 0)
