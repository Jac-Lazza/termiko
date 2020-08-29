#author: n01
"""
Useful Keyboard keys
"""
# UP = "\x1b[A"
# DOWN = "\x1b[B"
# RIGHT = "\x1b[C"
# LEFT = "\x1b[D"
UP = "W"
LEFT = "A"
DOWN = "S"
RIGHT = "D"
ENTER = "\r"
# ARROW_PREP = ('\x1b', '[') #Not needed anymore
# ESC = "\x1b" #Now this keys can be finnaly hit EDIT: no, it has problems between platforms
QUIT = "Q"
# DELETE = '\x7f' #This seems terminal-specifics
DELETE = "\x08"
#Some terminals use delete code characters different from \x08 (the standard one), this is strange and I still have to understand why they do this
BAD_DELETES = ["\x7f"]

KEYS = [UP, DOWN, RIGHT, LEFT, ENTER, DELETE, QUIT]
