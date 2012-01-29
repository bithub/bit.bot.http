
from zope.interface import implements
from zope.component import getUtility, queryAdapter
from twisted.web import server
from twisted.web.resource import Resource

from bit.bot.common.interfaces import IHTTPRoot, IHTTPResource

class HTTPRoot(Resource):
    implements(IHTTPRoot)
    def render_GET(self, request):
        return 'hello there!'

    def getChild(self,name,request):
        if name == '':
            return self
        return queryAdapter(self,IHTTPResource,name)
        return WebSession()
    
