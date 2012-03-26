import json

from zope.component import getUtility, queryAdapter
from zope.interface import implements
from zope.event import notify

from twisted.python import log

from bit.core.interfaces import ICommand
from bit.bot.common.interfaces import IIntelligent, ISessions,\
    ISubscriptions, IMembers
from bit.bot.http.events import ClientAuthEvent
from bit.bot.http.interfaces import IHTTPSocketRequest


class SocketRequest(object):
    def __init__(self, proto):
        self.proto = proto


class AuthRequest(SocketRequest):
    implements(IHTTPSocketRequest)

    def load(self, sessionid, sess, data):
        log.msg('bit.bot.http.request: AuthRequest.load ', data['message'])
        kernel = getUtility(IIntelligent).bot

        def _gotSession(sess):
            kernel.setPredicate('secure', "yes", sess.jid)
            kernel.setPredicate('name', personname, sess.jid)
            self.proto.speak(sess.jid, 'welcome %s' % personname, anon_jid)
            return getUtility(ISessions).activate(self.proto, sess)

        def _gotPersonSessions(sessions, anon_jid, person):
            # there could be many, but we'll take the first one,
            # we should check which was last accessed
            for session in sessions:
                kernel.setPredicate('secure', "yes", session.jid)
                kernel.setPredicate('name', personname, session.jid)
                self.proto.speak(anon_jid, 'welcome %s' % person.id, anon_jid)
                return getUtility(ISessions).activate(self.proto, session)
            # ok no existing session, lets add one
            session_id = anon_jid.split('/')[1]
            person_jid = '%s/%s' % (person.jid, session_id)
            getUtility(ISessions).add_session(
                session_id=sessionid, jid=person_jid, session_type='curate'
                ).addCallback(_gotSession)

        def _gotThisSession(sessions, anon_jid, person):
            for session in sessions:
                kernel.setPredicate('secure', "yes", session.jid)
                kernel.setPredicate('name', person.id, session.jid)
                self.proto.speak(anon_jid, 'welcome %s' % person.id, anon_jid)
                return getUtility(ISessions).activate(self.proto, session)

            session_id = anon_jid.split('/')[1]
            person_jid = '%s/%s' % (person.jid, session_id)

            # ok, this isnt a saved session,
            # does this user have another saved bot sesssion?
            getUtility(ISessions).sessions(
                person=person_jid.split('/')[0], session_type="curate"
                ).addCallback(_gotPersonSessions, anon_jid, person)

        def isauth(person, personname, anon_jid):
            if not person:
                self.proto.speak(anon_jid,
                                 "I've no idea who you are,"
                                 + "but good luck being %s" % personname,
                                 anon_jid)
                return

            sessions = getUtility(ISessions)
            session_id = anon_jid.split('/')[1]
            person_jid = '%s/%s' % (person.jid, session_id)

            # is this session an existing session?
            sessions.sessions(
                jid=person_jid, session_type="curate"
                ).addCallback(_gotThisSession, anon_jid, person)

        anon_jid = 'anon@chat.3ca.org.uk/%s' % sessionid
        personname = kernel.getPredicate(
            kernel._inputHistory, anon_jid)[-1:].pop().strip()
        return getUtility(IMembers).auth(
            personname, data['password'].strip()
            ).addCallback(isauth, personname, anon_jid)


class MessageRequest(SocketRequest):
    implements(IHTTPSocketRequest)

    def response(self, msg):
        log.msg('bit.bot.http.request: MessageRequest.response: ', msg)
        self.proto.transport.write(json.dumps(msg))

    def load(self, sessionid, sess, data):
        log.msg('bit.bot.http.request: MessageRequest.load: ', data['message'])
        kernel = getUtility(IIntelligent).bot

        if sess:
            self.session_id = sess.jid
            getUtility(ISessions).stamp(sessionid)
            #notify(SocketSessionEvent(self).update(sessionid))
            kernel.setPredicate('secure', "yes", sess.jid)
            kernel.setPredicate('name', sess.jid.split('@')[0], sess.jid)
            return getUtility(IIntelligent).respond(
                self, data['message'].strip()).addCallback(self.speak)
        self.session_id = 'anon@chat.3ca.org.uk/%s' % sessionid
        return getUtility(IIntelligent).respond(
            self, data['message'].strip()).addCallback(self.speak)

    def speak(self, msg):
        log.msg('bit.bot.http.request: MessageRequest.speak ', msg)
        self.response(dict(emit={'respond': msg}))


class SubscribeRequest(SocketRequest):
    implements(IHTTPSocketRequest)

    def load(self, sessionid, sess, data):
        log.msg('bit.bot.http.request: SubscribeRequest.load ',
                data['message'])
        getUtility(ISubscriptions).subscribe(
            data['subscribe'], sessionid, self.proto.transport.write)


class HeloRequest(SocketRequest):
    implements(IHTTPSocketRequest)

    def load(self, sessionid, sess, data):
        log.msg('bit.bot.http.request: HeloRequest.load ', sessionid)
        notify(ClientAuthEvent(self.proto).update(sessionid, data, sess))


class CommandRequest(SocketRequest):
    implements(IHTTPSocketRequest)

    def response(self, msg):
        log.msg(
            'bit.bot.http.request: CommandRequest.response ', msg)
        self.proto.transport.write(json.dumps(msg))

    def load(self, sessionid, sess, data):
        log.msg('bit.bot.http.request: CommandRequest.load: ',
                sessionid, data['message'])
        self.session_id = sessionid
        msg = data['command']
        command_name = msg.strip().split(' ')[0]
        command = queryAdapter(self, ICommand, command_name)
        self.session_id = sessionid
        if not command:
            command = queryAdapter(self, ICommand)
            msg = 'help %s' % command_name
        return command.load(sessionid, msg).addCallback(self.response)

    def speak(self, msg):
        log.msg('bit.bot.http.request: CommandRequest.speak ', msg)
        self.response(dict(emit={'respond': msg}))
