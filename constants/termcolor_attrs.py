#author: n01
"""
Useful termcolor attributes (attrs for short)
@Usage: colored("stringa", COLOR, attrs=ATTRIBUTE)
These attributes are list with a single element
to create longer list just add the attributes together
e.g. BLINK + BOLD gives you ['blink', 'bold']
"""

BLINK = ["blink"]
BOLD = ["bold"]
DARK = ["dark"]
UNDERLINE = ["underline"]
REVERSE = ["reverse"]
CONCEALED = ["concealed"]

NO_ATTRS = [] #Empty list when you don't want effects to be applied

ATTRS = [BLINK, BOLD, DARK, UNDERLINE, REVERSE, CONCEALED, NO_ATTRS]
