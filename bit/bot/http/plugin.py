
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




