#author: n01
"""
Messages are all the different writings that a user shall come across while
interacting with the main interface of the program
"""
# from termcolor import colored
# from colorama import init as colorama_init
# from constants.constants import *
from local_imports import *
from misc import *

###

# def welcome_message():
#     print(colored("TERMIKO!", "cyan")) #TO MODIFY

# def main_menu(selected=0):
#     avaiable_columns = get_avaiable_columns()
#     MENU = [x.center(avaiable_columns, " ") for x in MENU_TEXT]
#     clear()
#     welcome_message()
#     for i in range(len(MENU)):
#         if(i==selected):
#             print(colored(MENU[i], CYAN, "on_magenta"))
#         else:
#             print(colored(MENU[i], MAGENTA))
#     command = readArrow()
#     if(command == DOWN):
#         selected = (selected+1)%len(MENU)
#     elif(command == UP):
#         selected -= 1
#         if(selected < 0):
#             selected = len(MENU)-1
#     elif(command == ENTER):
#         return selected
#     return menu(selected)

def main_menu(text, selected=0):
    # MENU = ["Local match", "Network match", "Game rules", "Options", "Exit"] #Temporal, must be read by configuration file
    return menu(text, selected=selected, optional_text="TERMIKO!")
