import doctest

from twisted.trial import runner


test_configuration = """
[bit]
name = testbot
plugins = bit.bot.http
"""


def setUp(self):
    pass


def test_suite():
    ts = runner.TestSuite()
    ts.name = "bit.bot.http.doctests"
    ts.addTest(doctest.DocFileSuite(
            "../README.txt", setUp=setUp,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE))
    return ts
