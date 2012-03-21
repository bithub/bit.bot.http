import json

from zope.component import adapter, getUtility

from bit.core.interfaces import ISockets
from bit.bot.common.interfaces import ISubscriptions, IFlatten
from bit.bot.http.events import SocketCreatedEvent,\
    SocketLostEvent, ClientAuthEvent


def socket_updated(evt):
    print 'SOCKET UPDATE'
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
    socket_updated(evt)


@adapter(SocketLostEvent)
def socket_lost(evt):
    socket_updated(evt)


@adapter(ClientAuthEvent)
def client_auth(evt):
    return evt.socket.transport.write(
        json.dumps(dict(
                emit={'helo': ''},
                bit=dict(
                    bot=dict(
                        session=(dict(jid='anon@chat.3ca.org.uk/'
                                      + evt.session_id,
                                      persistent=False
                                      )))))))
    evt.socket.transport.write(
        json.dumps(dict(emit={'helo': ''},
                        bit=dict(bot=dict(session=(dict(jid=evt.session.jid,
                                                        persistent=True
                                                        )))))))
