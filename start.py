from sys import flags

if not flags.interactive:
    print("I need to be imported in an interactive python console. Try 'start' instead of 'start.py'")
    quit()

from frontend import *
