

from twisted.internet.protocol import Factory, Protocol

policy = """                                                                                                                                                                                                   
<cross-domain-policy>                                                                                                                                                                                          
    <allow-access-from domain="*" to-ports="*" />                                                                                                                                                              
</cross-domain-policy>                                                                                                                                                                                         
"""

class PolicyProtocol(Protocol):

    def connectionMade(self):
        import pdb; pdb.set_trace()
        self.transport.write(policy)
        self.transport.loseConnection()

class FlashPolicyFactory(Factory):
    protocol = PolicyProtocol
