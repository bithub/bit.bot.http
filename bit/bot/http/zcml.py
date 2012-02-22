
import zope
import os
import bit

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('bit.core')

class IHTTPDirective(zope.interface.Interface):
    """
    Define a http
    """
    filepath = zope.configuration.fields.Path(
        title=_("File path"),
        description=_("The directory system file path"),       
        required=True,
        )
    path = zope.schema.TextLine(
        title=_("Path"), 
        description=_("The http path"),       
        required=False,
        )

def http(_context, filepath, path=None):
    for rtype in os.listdir(filepath):
        resource = zope.component.queryUtility(bit.bot.common.interfaces.IHTTPRoot,rtype)
        if not resource: continue
        _context.action(
            discriminator = None,
            callable = resource.add_resources,
            args = (os.path.join(filepath,rtype),)
            )
        

