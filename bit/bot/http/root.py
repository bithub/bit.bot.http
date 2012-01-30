
from zope.interface import implements
from zope.component import getUtility, queryAdapter, queryUtility
from twisted.web import server
from twisted.web.resource import Resource

from bit.bot.common.interfaces import IHTTPRoot, IHTTPResource, IWebRoot

class HTTPRoot(Resource):
    implements(IHTTPRoot)
    def render_GET(self, request):
        return 'hello there!'

    def getChild(self,name,request):
        if name == '':
            web = queryUtility(IWebRoot)
            return web or self
        return getUtility(IHTTPRoot,name)
