import os
from zope.interface import implements
from zope.component import getUtility
from bit.bot.common.interfaces import IPluginFactory, IApplication, IServices, IHTTPRoot, IIntelligent

from twisted.application.strports import service as tcpservice
from twisted.application.internet import TCPServer

from bit.bot.base.plugin import BitBotPluginBase


class BotPeople(BitBotPluginBase):
    implements(IPluginFactory)
    name = 'bit.bot.people'
