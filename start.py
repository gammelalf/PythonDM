from sys import flags as __flags

if not __flags.interactive:
    print("I need to be imported in an interactive python console. Try 'start' instead of 'start.py'")
    quit()

from frontend.__init__ import *
