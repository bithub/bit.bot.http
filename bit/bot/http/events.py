


class SocketCreatedEvent(object):
    def __init__(self,bot):
        self.bot = bot

    def update(self,sessionID):
        self.session_id = sessionID
        return self

        
class SocketLostEvent(object):
    def __init__(self,bot):
        self.bot = bot

    def update(self,sessionID,reason):
        self.session_id = sessionID
        self.reason = reason
        return self

