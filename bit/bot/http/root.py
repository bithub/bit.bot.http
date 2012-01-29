
from zope.interface import implements
from zope.component import getUtility
from twisted.web import server
from twisted.web.resource import Resource

from bit.bot.common.interfaces import IHTTPRoot, IHTTPResource, IWebHTML

class HTTPRoot(Resource):
    implements(IHTTPRoot)
    def render_GET(self, request):
        html = getUtility(IWebHTML)
        return html.children['bot.html'].render_GET(request)

    def getChild(self,name,request):
        if name == '':
            return self
        return queryAdapter(IHTTPResource,self,name=name)
        return WebSession()
    
