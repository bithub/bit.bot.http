
from OpenSSL import SSL

from zope.interface import implements
from zope.component import getUtility, provideAdapter
from twisted.web import server
from twisted.application.internet import TCPServer, SSLServer

from bit.core.interfaces import IConfiguration, IPlugin, ISockets, IPluginExtender
from bit.bot.common.interfaces import IHTTPRoot, IWebRoot, IFlatten, IBotSocket, ISocketRequest, IResourceRegistry

from bit.bot.base.plugin import BotPlugin
from bit.bot.http.root import HTTPRoot
from bit.bot.http.socket import WebBotSocketFactory, Sockets
from bit.bot.http.request import AuthRequest, SubscribeRequest, MessageRequest, HeloRequest, CommandRequest
from bit.bot.http.handlers import socket_created, socket_lost
from bit.bot.http.flat import SocketsFlattener
from bit.bot.http.extends import HTTPPlugin

from bit.bot.http.policy import FlashPolicyFactory

class SSLContextFactory(object):
   def getContext(self):
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_certificate_file(getUtility(IConfiguration).get('https','cert'))
        ctx.use_privatekey_file(getUtility(IConfiguration).get('https','key'))
        return ctx    

class BotHTTP(BotPlugin):
    implements(IPlugin)
    name = 'bit.bot.http'
    _handlers = [socket_created,socket_lost]        
    _utils = [(Sockets(),ISockets)
              ,(HTTPRoot(),IHTTPRoot)]              
    _http = {'root': 'resources'}

    def load_services(self):
        self._services = {'wss': dict( service=SSLServer
                                       ,args=[int(getUtility(IConfiguration).get('wss','port'))
                                              ,WebBotSocketFactory()
                                              ,SSLContextFactory()])
                          ,'flash-policy': dict( service=TCPServer
                                                 ,args=[843,FlashPolicyFactory()])
                          ,'https': dict( service = SSLServer 
                                         ,args =[int(getUtility(IConfiguration).get('https','port'))
                                                 ,server.Site(getUtility(IHTTPRoot))
                                                 ,SSLContextFactory()])
                          }
        super(BotHTTP,self).load_services()        

    def load_adapters(self):
        provideAdapter(HTTPPlugin,[IPlugin,],IPluginExtender,'http')        
        provideAdapter(SocketsFlattener,[ISockets,],IFlatten)        
        provideAdapter(AuthRequest,[IBotSocket,],ISocketRequest,name='auth')        
        provideAdapter(MessageRequest,[IBotSocket,],ISocketRequest,name='message')        
        provideAdapter(CommandRequest,[IBotSocket,],ISocketRequest,name='command')        
        provideAdapter(SubscribeRequest,[IBotSocket,],ISocketRequest,name='subscribe')        
        provideAdapter(HeloRequest,[IBotSocket,],ISocketRequest,name='helo')        


    def load_JS(self):
       js = getUtility(IResourceRegistry,'js')
       js.add('jquery-min.js',{'rel':'link'})
