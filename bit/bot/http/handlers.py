import json

from zope.component import adapter, getUtility

from twisted.python import log

from bit.core.interfaces import ISockets
from bit.bot.common.interfaces import ISubscriptions, IFlatten
from bit.bot.http.events import SocketCreatedEvent,\
    SocketLostEvent, ClientAuthEvent


def socket_updated(evt):
    subs = getUtility(ISubscriptions)

    def _gotSockets(sockets):
        if 'sockets-changed' in subs.subscriptions:
            print 'subscriber!'
            for subscriber in subs.subscriptions['sockets-changed']:
                subs.subscriptions['sockets-changed'][subscriber](
                    json.dumps(dict(
                            emit={'sockets-changed': 'Sockets changed'},
                            bit=dict(bot=dict(admin=(dict(sockets=sockets))))
                            )))
    IFlatten(getUtility(ISockets)).flatten().addCallback(_gotSockets)


@adapter(SocketCreatedEvent)
def socket_created(evt):
    log.msg('bit.bot.http.handlers: socket_created')
    socket_updated(evt)


@adapter(SocketLostEvent)
def socket_lost(evt):
    log.msg('bit.bot.http.handlers: socket_lost')
    socket_updated(evt)


@adapter(ClientAuthEvent)
def client_auth(evt):
    log.msg('bit.bot.http.handlers: socket_auth')
    evt.socket.transport.write(
        json.dumps(dict(emit={'helo': ''},
                        token=evt.session.token,
                        session=evt.session.hex,
                        bit=dict(bot=dict(session=(dict(owner=evt.session.owner,
                                                        token=evt.session.token,
                                                        persistent=True
                                                        )))))))
