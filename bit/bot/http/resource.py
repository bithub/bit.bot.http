
import os

from twisted.web import static
from twisted.web.resource import Resource


class BotResource(Resource):

    def __init__(self):
        Resource.__init__(self)

    def render_GET(self, request):
        return "<dl>%s</dl>" %''.join(["<dt>%s</dt><dd>%s</dd>"%(k,v) for k,v in self.children.items()])

    _ext = []
    def add_resources(self,dir_target,parent=None):
        from bit.bot.http.folder import BotFolder
        for f in os.listdir(dir_target):
            if os.path.isdir(os.path.join(dir_target,f)): continue
            for ext in self._ext:
                if f.endswith('.%s'%ext):
                    file_path = os.path.join(dir_target,f)
                    print 'adding resource: %s' %file_path                    
                    if file_path.endswith('bot.html'):
                        import pdb; pdb.set_trace()
                    (parent or self).putChild(f,static.File(file_path))        

        for subf in os.listdir(dir_target):
            if os.path.isdir(os.path.join(dir_target,subf)):
                if not subf in (parent or self).children:
                    (parent or self).putChild(subf,BotFolder())
                subresource = (parent or self).children[subf]
                self.add_resources(os.path.join(dir_target,subf),subresource)

