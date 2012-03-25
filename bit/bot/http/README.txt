bit.bot.http
============

    >>> import bit.bot.base

Lets start by creating a configuration for our app    

    >>> test_configuration = """
    ... [bit]
    ... name = testapp
    ... plugins = bit.bot.http
    ... 
    ... [http]
    ... port = 1026    
    ... 
    ... [ws]
    ... port = 8382
    ... 
    ... [https]
    ... port = 1027    
    ... 
    ... [wss]
    ... port = 8383
    ... 
    ... [flash-policy]
    ... port = 3838
    ... 
    ... """

Lets initialize the app environment

    >>> sc = bit.bot.base.tap.makeServiceFromString(test_configuration)

Our http multi-service has been registered with the applications service collection

    >>> sc.namedServices.keys()
    [u'bit.bot.http']

    >>> import zope

We can also get to our services with the IServices utility

    >>> services = zope.component.getUtility(bit.core.interfaces.IServices)
    >>> http_multi = services.services['bit.bot.http']
    >>> http_multi
    <twisted.application.service.MultiService instance ...>


bit.bot.http.services
---------------------

    >>> sorted(http_multi.namedServices.keys())
    [u'flash-policy', u'http', u'https', u'ws', u'wss']

    >>> http_service = http_multi.getServiceNamed('http')
    >>> http_service
    <twisted.application.internet.TCPServer ...>

    >>> http_service.args
    (1026, <twisted.web.server.Site instance ...>)

    >>> http_site = http_service.args[1]
    >>> http_site
    <twisted.web.server.Site instance ...>

    >>> http_resource = http_site.resource
    >>> http_resource
    <bit.bot.http.root.HTTPRoot instance ...>
    
    >>> bit.bot.http.interfaces.IHTTPRoot.providedBy(http_resource)
    True


fetching a web page
-------------------

    >>> import twisted.web.client
    >>> def got_page(resp):
    ...	    if not 'hello there!' == resp:
    ...	       print 'ERROR: loading page failed'

    >>> d = twisted.web.client.getPage('http://localhost:1026')
    >>> d.addCallback(got_page)
    <Deferred at ...>

Lets create a helper for running zcml through

  >>> from cStringIO import StringIO
  >>> from zope.configuration.xmlconfig import xmlconfig
  >>> def runSnippet(snippet):
  ...     template = """\
  ...     <configure xmlns='http://namespaces.zope.org/zope'
  ...                i18n_domain="zope">
  ...     %s
  ...     </configure>"""
  ...     xmlconfig(StringIO(template % snippet))


twisted
-------

Lets get ready to stop twisted, 8)

   >>> _d = d.addCallbacks(lambda x: None)
   >>> _d = d.addCallbacks(lambda x: twisted.internet.reactor.stop())

And start it!

   >>> twisted.internet.reactor.run()
