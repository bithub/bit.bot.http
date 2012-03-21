

class SocketCreatedEvent(object):
    def __init__(self, bot):
        self.bot = bot

    def update(self, sessionID):
        self.session_id = sessionID
        return self


class SocketLostEvent(object):
    def __init__(self, bot):
        self.bot = bot

    def update(self, sessionID, reason):
        self.session_id = sessionID
        self.reason = reason
        return self


class ClientAuthEvent(object):
    def __init__(self, socket):
        self.socket = socket

    def update(self, session_id, data, sess):
        self.session_id = session_id
        self.data = data
        self.session = sess
        return self
