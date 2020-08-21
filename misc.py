#author: n01
"""
Miscellaneus functions
"""
# import sys
# import os
# from constants.constants import *
# from readchar import readchar #Useful for reading a single character
from local_imports import *


#Definition of the clearing command
CLEARING_COMMAND = "clear" #System command to clear the screen
if(sys.platform == "win32"):
    CLEARING_COMMAND = "cls" #Windows uses cls, the rest of the world uses clear

def clear():
    """
    Used for cleaning the screen
    """
    os.system(CLEARING_COMMAND)
    # if(sys.platform == "win32"):
    #     os.system("cls")
    # else:
    #     os.system("clear")

def get_avaiable_columns():
    """
    Get avaiable terminal columns
    """
    return os.get_terminal_size()[0]

def get_avaiable_rows():
    """
    Get avaiable terminal rows
    """
    return os.get_terminal_size()[1]

# def get_textbox_size():
#     """
#     The maximum size of a textbox in this game (10% of the avaiable columns)
#     Used in the MapManager buffer lines
#     """
#     return get_avaiable_columns()*10//100

def buffer_line_pad(text):
    """
    Pad a message for a MapManager bufferline by adding ': ' at the end of text
    and making the string occupy the 10% of the avaiable columns
    """
    max_padding = get_avaiable_columns()*10//100
    text += ": "
    return text + " "*(max_padding-len(text))

# def readArrow():
#     """
#     Used to read a single character from the screen,
#     in this case the keyboard arrows
#     """
#     try:
#         value = readchar()
#         if(value == ENTER):
#             return ENTER
#         elif(value == DELETE):
#             return DELETE
#         elif(value == ARROW_PREP[0]):
#             if(readchar() == ARROW_PREP[1]):
#                 value = readchar()
#                 if(value == 'A'):
#                     return UP
#                 elif(value == 'B'):
#                     return DOWN
#                 elif(value == 'C'):
#                     return RIGHT
#                 elif(value == 'D'):
#                     return LEFT
#     except Exception as e:
#         return None

def readArrow():
    """
    The usage of readchar gave problems between platofrm, and it was more complicated
    to read the directional arrows. The correct function to read a key pressing is
    readchar.readkey(), the function that I'm now using
    """
    try:
        value = readkey()
        value = value.upper() #For the 'Q' key
        if(value in KEYS):
            return value
    except:
        pass
    return None

def put(data):
    print(data, end="")

def resolve_newline(data):
    """
    Newline problem: Unix platforms puts a \n as terminator, Windows does not
    This function resolves this problem once and for all
    @data: is a list of strings
    """
    if(data[len(data)-1] == ''):
        #Newline detected
        data = data[:len(data)-1]
    return data

def menu(menu_text, selected=0, optional_text=None):
    """
    Low level function for a generic menu generation
    @optional_text is used only in the main menu
    """
    avaiable_columns = get_avaiable_columns()
    text = [x.center(avaiable_columns, " ") for x in menu_text]
    clear()
    if(optional_text != None):
        print(colored(optional_text.center(avaiable_columns, " "), CYAN, attrs=BOLD)) #Change the logic, need of ASCII art
    for i in range(len(text)):
        if(i==selected):
            print(colored(text[i], CYAN, "on_magenta"))
        else:
            print(colored(text[i], MAGENTA))
    command = readArrow()
    if(command == DOWN):
        selected = (selected+1)%len(text)
    elif(command == UP):
        selected -= 1
        if(selected < 0):
            selected = len(text)-1
    elif(command == ENTER):
        return selected
        #Maybe to add something
    elif(command == DELETE):
        return DELETE
    elif(command == QUIT):
        return QUIT
    return menu(menu_text, selected, optional_text)

# def toggle_visibility():
#     """
#     This function is strange. Its existance araise from the way I have implemented
#     previuos code. So I need to change a global variable (the NO_ATTRS) to be concealed.
#     Maybe it is not the best way to write code, let's hope it works
#     """
#     #I'm having a bad time with the global keyword, we don't understand each other
#     global NO_ATTRS
#     if(NO_ATTRS == []):
#         NO_ATTRS = CONCEALED
#     else:
#         NO_ATTRS = []

# def disable_visibility():
#     global NO_ATTRS
#     NO_ATTRS = CONCEALED
#
# def enable_visibility():
#     global NO_ATTRS
#     NO_ATTRS = []
