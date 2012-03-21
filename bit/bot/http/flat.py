from zope.interface import implements

from twisted.internet import defer

from bit.bot.common.interfaces import IFlatten
from bit.bot.base.flat import Flattener


class SocketsFlattener(Flattener):
    implements(IFlatten)

    def flatten(self):
        _sockets = {}
        sockets = self.context.sockets
        for socket in sockets:
            _sockets[socket] = []
            for _socket in sockets[socket]:
                _sockets[socket].append(_socket)
        return defer.maybeDeferred(lambda: _sockets)
