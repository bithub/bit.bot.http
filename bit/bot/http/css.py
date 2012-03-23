from zope.interface import implements, implementer
from zope.component import getUtility, getAdapter

from bit.bot.common.interfaces import IWebCSS, IWebResource
from bit.bot.http.interfaces import  IResourceRegistry, IHTTPRoot, IHTTPResource
from bit.bot.http.resource import BotResource
from bit.bot.http.registry import ResourceRegistry


class WebCSS(object):
    implements(IWebResource)
    _meta = {}

    def __init__(self, resource):
        self.resource = resource

    def update(self, upd):
        self._meta.update(upd)

    def render(self):
        return '<link rel="%s" type="%s" href="/css/%s" />\n'\
            % ("stylesheet",
               "text/css",
               self._meta['path'])


class CSSRegistry(ResourceRegistry):
    implements(IResourceRegistry)
    _resources = []
    _res_meta = {}

    def add(self, resid, options):
        self._resources.append(resid)
        if options:
            self._res_meta[resid] = options

    @property
    def resources(self):
        css = getUtility(IHTTPRoot, 'css')
        for resid in self._resources:
            if resid in css.children:
                resource = IWebResource(css)
                resource.update(dict(path=resid,
                                     resource=css.children[resid]))
                if resid in self._res_meta:
                    resource.update(self._res_meta[resid])
                yield resource


css_registry = CSSRegistry()


class BotCSS(BotResource):
    implements(IWebCSS, IHTTPResource)
    _ext = ['css']

    def __init__(self, root):
        self.root = root
        BotResource.__init__(self)


@implementer(IHTTPRoot)
def botCSS():
    root = getUtility(IHTTPRoot)
    return getAdapter(root, IHTTPResource, 'css')
