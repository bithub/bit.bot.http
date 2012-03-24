from zope.interface import Interface as I

from bit.bot.common.interfaces import ISocketRequest


class IHTTPRoot(I):
    pass


class IHTTPResource(I):
    pass


class IHTMLResources(I):
    pass


class IResourceRegistry(I):
    pass


class IHTTPSocketRequest(ISocketRequest):
    """ an HTTP request object """
