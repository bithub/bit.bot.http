import os

import zope

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
        resource = zope.component.queryUtility(
            bit.bot.http.interfaces.IHTTPRoot, rtype)
        if not resource:
            continue
        _context.action(
            discriminator=None,
            callable=resource.add_resources,
            args=(os.path.join(filepath, rtype), )
            )


class ICSSDirective(zope.interface.Interface):
    """
    Define a css
    """
    name = zope.schema.TextLine(
        title=_("CSS file name"),
        description=_("The name of this CSS resource"),       
        required=True,
        )
    rel = zope.schema.TextLine(
        title=_("Relationship"), 
        description=_("The css path"),       
        required=False,
        )


def css(_context, name, rel=None):
    _context.action(
        discriminator=None,
        callable=zope.component.getUtility(
            bit.bot.common.interfaces.IResourceRegistry, 'css').add,
        args=(name, {'rel': rel or 'link'})
        )


class IJSDirective(zope.interface.Interface):
    """
    Define a js
    """
    name = zope.schema.TextLine(
        title=_("JS file name"),
        description=_("The name of this JS resource"),       
        required=True,
        )
    rel = zope.schema.TextLine(
        title=_("Relationship"), 
        description=_("The js path"),       
        required=False,
        )


def js(_context, name, rel=None):
    _context.action(
        discriminator=None,
        callable=zope.component.getUtility(
            bit.bot.common.interfaces.IResourceRegistry, 'js').add,
        args=(name, {'rel': rel or 'link'})
        )
