"""
This is a helper module.
Its purpose is to supply tools that are used to generate version specific code.
Goal is to generate code that work on both python2x and python3x.
"""
from numpy import generic as npscalar
from numpy import ndarray as nparray
from sys import version_info as pyver
from sys import platform as sysplatform
from os import name as osname


isposix = osname == 'posix'
isnt = osname == 'nt'
islinux = sysplatform.startswith('linux')
iswin = sysplatform.startswith('win')

if isposix:
    tmpdir = "/tmp/"
else:
    from os import getenv as tmpdir
    tmpdir = tmpdir('TEMP')+'\\'

ispy3 = pyver > (3,)
ispy2 = pyver < (3,)

# __builtins__ is dict
try:
    has_long = 'long' in __builtins__#.__dict__.keys()
    has_unicode = 'unicode' in __builtins__#.__dict__.keys()
    has_basestring = 'basestring' in __builtins__#.__dict__.keys()
    has_bytes = 'bytes' in __builtins__#.__dict__.keys()
    has_buffer = 'buffer' in __builtins__#.__dict__.keys()
    has_xrange = 'xrange' in __builtins__#.__dict__.keys()
except:
    has_long = 'long' in __builtins__.__dict__.keys()
    has_unicode = 'unicode' in __builtins__.__dict__.keys()
    has_basestring = 'basestring' in __builtins__.__dict__.keys()
    has_bytes = 'bytes' in __builtins__.__dict__.keys()
    has_buffer = 'buffer' in __builtins__.__dict__.keys()
    has_xrange = 'xrange' in __builtins__.__dict__.keys()
# end try

# substitute missing builtins
if has_long:
    long = long  # analysis:ignore
else:
    long = int
# end if

if has_basestring:
    basestring = basestring  # analysis:ignore
elif has_bytes:
    basestring = (str, bytes)
else:
    basestring = str
# end if

if has_unicode:
    unicode = unicode  # analysis:ignore
else:
    unicode = str
# end if

if has_bytes:
    bytes = bytes  # analysis:ignore
else:
    bytes = str
# end if

if has_buffer:
    buffer = buffer  # analysis:ignore
else:
    buffer = memoryview
# end if

if has_xrange:
    xrange = xrange  # analysis:ignore
    range = range
else:
    xrange = range
    range = lambda *x: list(__builtins__['range'](*x))
# end if

if ispy3:
    numbers = (int, float, complex)
else:
    numbers = (int, float, long, complex)  # analysis:ignore
# end if

if ispy3:
    from _io import TextIOWrapper as file
    import urllib.request as urllib
    from itertools import zip_longest
    import queue
    import configparser as ConfigParser
else:
    file = file
    import urllib2 as urllib  # analysis:ignore
    from itertools import izip_longest as zip_longest  # analysis:ignore
    import Queue as queue # analysis:ignore
    import configparser
# end if

try:
    import cPickle as pickle
except:
    import pickle  # analysis:ignore
# end try

# helper variant string
if has_unicode:
    varstr = unicode
else:
    varstr = bytes
# end if

def _decode(string):
    try:
        return string.decode('utf-8', 'backslashreplace')
    except:
        return string.decode('CP1252', 'backslashreplace')
    # end try
# end def

def _encode(string):
    try:
        return string.encode('utf-8')
    except:
        return string.encode('CP1252')
    # end try
# end def

# numpy char types
npunicode = 'U'
npbytes = 'S'


if ispy2:
    npstr = npbytes
else:
    npstr = npunicode
# end if

def _tostring(string, targ, nptarg, conv):
    if isinstance(string, targ):  # short cut
        return targ(string)
    if isinstance(string, basestring):
        return targ(conv(string))
    if isinstance(string, (list, tuple)):
        return type(string)(_tostring(s, targ, nptarg, conv) for s in string)
    if isinstance(string, npscalar):
        return targ(string.astype(nptarg))
    if isinstance(string, nparray):
        string = string.astype(nptarg).tolist()
    return _tostring(str(string), targ, nptarg, conv)


def tostr(string):
    if ispy2:
        return tobytes(string)
    else:
        return tounicode(string)


def tobytes(string):
    return tounicode(string).encode('utf-8', 'backslashreplace')



def tounicode(string):
    return _tostring(string, unicode, npunicode, _decode)


