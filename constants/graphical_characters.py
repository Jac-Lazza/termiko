#author: n01
"""
Graphical characters are the Unicode escape sequences to be used to
print symbols on both Windows and Linux platorm

Personal Note:
I'm lucky to have started the project on a system and a terminal that could
answer to my creativity. I must know try to adjust the whole thing for lesser fortunate
terminals out there. Windows is a special case of love and hate, more hate than love.
"""
from sys import platform

BLOCK_1 = "\u2591" # ░
BLOCK_2 = "\u2592" # ▒
BLOCK_3 = "\u2593" # ▓
BLOCK = "\u2588" # █

BLOCKS = [BLOCK_1, BLOCK_2, BLOCK_3, BLOCK]

BULLET_BLOCK = "\u2589" # ▉ ~ ▉▉▉
CHESS_BLOCK = " " + "\u259E"*3 + " " # ▞▞▞

if(platform == "win32"):
    BULLET_BLOCK = BLOCK #Windows doesn't support the character
    CHESS_BLOCK = " --- " #Windows doesn't support also this character
