
from zope.component import getUtility

from twisted.web.resource import Resource
from bit.bot.common.interfaces import IWebImages, IWebCSS, IWebJS, IWebHTML, IWebJPlates

class BotHTTPRoot(Resource):

    def render_GET(self, request):
        html = getUtility(IWebHTML)
        return html.children['bot.html'].render_GET(request)

    def getChild(self,name,request):
        if name == '':
            return self

        if name == 'images':
            return getUtility(IWebImages)

        if name == 'js':
            return getUtility(IWebJS)

        if name == 'css':
            return getUtility(IWebCSS)

        if name == 'jplates':
            return getUtility(IWebJPlates)

        if name == '_html':
            return getUtility(IWebHTML)


