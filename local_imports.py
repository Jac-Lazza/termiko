#author: n01
"""
Imports file
"""

#System libraries
import os
import sys
import random
import time

#External libraries
from colorama import init as colorama_init #This function must be called on some platform to make ANSI colors enabled
from termcolor import colored #Function to create ASNI colored strings
from readchar import readchar #Library to read a single char, python does not provide an easy way to do this by default. too bad

#Local libraries
from constants.colors import *
from constants.keys import *
from constants.status import *
from constants.ignorable_characters import *
from constants.dirbases import *
from constants.termcolor_attrs import *
from constants.lang import *
from constants.settings import *

#Data structures
from constants.structures.id_structure import *
from constants.structures.options_structure import *
from constants.structures.translation_structure import *
from constants.structures.bonus_structure import *
from constants.structures.win_messages_structure import *
