# pyversion

This is a helper module for compatability between python 2 and python 3.  

Some modules have different behaviors or names between python versions.
ex //  
Instead of importing urllib from the module urllib, import it from pyversion 

Replace
"from pyversion import urllib as urllib"

Add this to the top of your modules:

# =========================================================================== #
# =========================================================================== #
# Try to handle most differences between python 2 and python 3 compatability
from __future__ import absolute_import, with_statement, absolute_import, \
                       division, print_function, unicode_literals
                       
