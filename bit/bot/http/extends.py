
import os, inspect

from zope.interface import implements
from zope.component import getUtility, provideAdapter, queryUtility
from bit.core.interfaces import IConfiguration, IPlugin, ISockets, IPluginExtender
from bit.bot.common.interfaces import IHTTPRoot

class HTTPPlugin(object):
   implements(IPluginExtender)
   def __init__(self,plugin):
      self.plugin = plugin

   def extend(self):
      if hasattr(self.plugin,'load_HTTP'):
         getattr(self.plugin,'load_HTTP')()      
      else:
         fpath =  os.path.dirname(inspect.getfile(self.plugin.__class__))
         http_paths = getattr(self.plugin,'_http',{})
         for hid,http in http_paths.items():
            if hid == 'root':
               target = os.path.join(fpath,http)
               for rtype in os.listdir(target):
                  resource = queryUtility(IHTTPRoot,rtype)
                  if not resource: continue
                  print 'adding %s %s' %(target,rtype)
                  resource.add_resources(os.path.join(target,rtype))


