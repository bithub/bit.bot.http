import json

from zope.component import getUtility, queryAdapter, getAdapter
from zope.interface import implements
from zope.event import notify

from twisted.python import log
from twisted.internet.protocol import Factory
from twisted.protocols.stateful import StatefulProtocol

from txws import WebSocketFactory

from bit.bot.common.interfaces import ISessions, IBotSocket, ISocketRequest
from bit.core.interfaces import ISockets
from bit.bot.http.events import SocketCreatedEvent, SocketLostEvent


class BotSocketProtocol(StatefulProtocol):
    implements(IBotSocket)

    def connectionMade(self):
        log.msg('bit.bot.http.socket: BotSocketProtocol.connectionMade')
        # send the current data model
        notify(SocketCreatedEvent(self))
        self.sessionid = None
        bit = {}
        bot = {}
        bot['base'] = {}
        bit['bot'] = bot
        emit = {}
        emit['connection-made'] = ''
        self.transport.write(json.dumps(dict(bit=bit, emit=emit)))

    def connectionLost(self, reason):
        log.msg('bit.bot.http.socket: BotSocketProtocol.connectionLost')
        notify(SocketLostEvent(self).update(self.sessionid, reason))
        if self.sessionid:
            getUtility(ISockets).remove('bot', self.sessionid, self)

    def dataReceived(self, data):
        log.msg('bit.bot.http.socket: BotSocketProtocol.dataReceived')
        data = json.loads(data)
        sessionid = data['session'].replace('-', '')
        self.sessionid = sessionid
        token = data.get('__bit_ac', None)
        if token:
            token = token.split('=')
            if token[0] == '__bit_ac' and len(token) > 1:
                token = token[1]

        def _gotSession(sess):
            log.msg(
                'bit.bot.http.socket: BotSocketProtocol.dataReceived._gotSession'
                ,sess)
            if sess:
                getUtility(ISockets).add('bot', sessionid, token, self)
            request = queryAdapter(self, ISocketRequest, name=data['request'])

            if data['request'] == 'message':
                message = data['message']
                if message.startswith('>'):
                    request = getAdapter(self, ISocketRequest, name="command")
                    message = message[1:]
                    data['command'] = message.strip().split(' ')[0]
                    data['args'] = ' '.join(message.strip().split(' ')[1:])
                elif message.startswith('~'):
                    request = getAdapter(
                        self, ISocketRequest, name="subscribe")
                    data['subscribe'] = message[1:]
                else:
                    request = getAdapter(
                        self, ISocketRequest, name="message")
            else:
                request = queryAdapter(
                    self, ISocketRequest, name=data['request'])

            if request:
                request.load(sessionid, sess, data)
            else:
                print 'NO REQUEST ADAPTER FOR: %s' % data['request']

        getUtility(ISessions).session(
            sessionid, token=token).addCallback(_gotSession)

    def getInitialState(self):
        pass

    def speak(self, jid, msg, asker):
        log.msg('bit.bot.http.socket: BotSocketProtocol.speak')
        self.transport.write(json.dumps(dict(emit={'respond': msg})))


class BotSocketFactory(Factory):
    protocol = BotSocketProtocol


class Sockets(object):
    implements(ISockets)
    _sockets = {}

    def add(self, socket_type, socket_id, token, socket):
        log.msg('bit.bot.http.socket: Sockets.add')
        if not socket_type in self._sockets:
            self._sockets[socket_type] = {}

        if not socket_id in self._sockets[socket_type]:
            self._sockets[socket_type][socket_id] = set()

        if not socket in self._sockets[socket_type][socket_id]:
            self._sockets[socket_type][socket_id].add(socket)

    def remove(self, socket_type, socket_id, token=None, socket=None):
        log.msg('bit.bot.http.socket: Sockets.remove')
        if not socket_type in self._sockets:
            return
        if not socket_id in self._sockets[socket_type]:
            return
        if socket in self._sockets[socket_type][socket_id]:
            self._sockets[socket_type][socket_id].remove(socket)
        if socket_id in self._sockets[socket_type]\
                and len(self._sockets[socket_type][socket_id]) == 0:
            del self._sockets[socket_type][socket_id]

    @property
    def sockets(self):
        return self._sockets

    def emit(self, socket_type, session_id,
             emmission, msg, token=None, bit_ac=None, bit={}, omit=[]):
        log.msg('bit.bot.http.socket: Sockets.emit')
        if not session_id in self.sockets[socket_type]:
            return
        for socket in self.sockets[socket_type][session_id]:
            if bit_ac:
                socket.transport.write(json.dumps(dict(emit={emmission: msg},
                                                       bit=bit,
                                                       __bit_ac=bit_ac,
                                                       )))
            else:
                socket.transport.write(json.dumps(dict(emit={emmission: msg},
                                                       bit=bit
                                                       )))


WebBotSocketFactory = lambda: WebSocketFactory(BotSocketFactory())
sockets = Sockets()
