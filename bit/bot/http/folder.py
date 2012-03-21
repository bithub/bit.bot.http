from zope.interface import implements

from bit.bot.common.interfaces import IWebFolder
from bit.bot.http.resource import BotResource


class BotFolder(BotResource):
    implements(IWebFolder)
