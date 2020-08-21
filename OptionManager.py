#author: n01
"""
OptionManager: Reads all the options, create specific structures for the read data
and provides method for accessing those pieces of data
"""
import json
from local_imports import *
from misc import *
from RulesManager import *

class OptionManager(object):

    def __init__(self):
        self.lang = None #Language of the game
        self.options = None #Current options
        self.translation = None #Translation of the game text
        # self.avaiable_troups = None
        # self.turn_limit = None
        # self.game_mode = None
        #Loading configuration and language resources
        self.read_default_lang()
        self.read_conf()
        self.read_text()
        #Reading the game rules in there language
        self.rules = RulesManager(self.lang)

    def read_default_lang(self):
        """
        Reads the default language from the file DEFAULT_LANG_PATH
        if the file is not found then it's created with the EN language
        if the file is malformed, then it's overwritten with the EN language
        """
        default_lang = EN
        try:
            with open(DEFAULT_LANG_PATH, "r") as file:
                default_lang = file.read()
            #Checking the read default_lang
            if(len(default_lang)<2):
                raise Exception("Dummy exception to enter the except clause")
            default_lang = default_lang[:2] #Taking the first two characters, avoiding CR or LF of all sorts
            if(not(default_lang in LANGS)):
                #Language not supported, use english
                raise Exception("Dummy exception to enter the except clause")
            #The lang read is avaiable
        except:
            #Can't read from file (probably)
            with open(DEFAULT_LANG_PATH, "w") as file:
                file.write(EN)
            default_lang = EN
        self.lang = default_lang

    def read_conf(self):
        """
        Reads configurations from OPTIONS_PATH
        """
        with open(OPTIONS_PATH, "r") as file:
            options_content = file.read()
        self.options = json.loads(options_content)

    def read_text(self):
        """
        Read the messages in the chosen languages
        (Must be called every time the language is changed)
        """
        lang_dirbase = LANG_FOLDER + self.lang + "/"
        with open(lang_dirbase + "translation.json", "r") as file:
            translation_content = file.read()
        self.translation = json.loads(translation_content)

    def save(self):
        """
        Save all configurations to their respectively files with
        their own structure
        """
        #Saving language
        with open(DEFAULT_LANG_PATH, "w") as file:
            file.write(self.lang)
        #Saving options
        options_content = json.dumps(self.options)
        with open(OPTIONS_PATH, "w") as file:
            file.write(options_content)

    def edit_options(self, selected=0):
        """
        This functions spawns a menu to change the options
        """
        options = list(self.translation[OPTIONS].values())
        options[0] += ": " + str(self.options[AVAIABLE_TROUPS])
        options[1] += ": " + str(self.options[TURN_LIMIT])
        gamemode_id = str(self.options[GAMEMODE])
        options[2] += ": " + self.translation[GAMEMODE][gamemode_id]
        # options[2] += ": " + str(self.options[GAMEMODE])
        options[3] += ": " + str(self.lang)
        continental_bonus_id = str(self.options[CONTINENTAL_BONUS])
        options[4] += ": " + self.translation[CONTINENTAL_BONUS][continental_bonus_id]
        # options[5] #Not modified, remeber that exists
        result = menu(options, selected=selected, optional_text=self.translation[GAME_OPTIONS])
        #Processing the result
        if(result == 0):
            self.options[AVAIABLE_TROUPS] = self.change_value(self.options[AVAIABLE_TROUPS], AVAIABLE_TROUPS_VALUES)
        elif(result == 1):
            self.options[TURN_LIMIT] = self.change_value(self.options[TURN_LIMIT], TURN_LIMIT_VALUES)
        elif(result == 2):
            self.options[GAMEMODE] = self.change_value(self.options[GAMEMODE], GAMEMODE_VALUES)
        elif(result == 3):
            self.lang = self.change_value(self.lang, LANGS)
            self.read_text()
            #Updating also the game rules
            self.rules.lang = self.lang
            self.rules.load_rules()
        elif(result == 4):
            self.options[CONTINENTAL_BONUS] = self.change_value(self.options[CONTINENTAL_BONUS], CONTINENTAL_BONUS_VALUES)
        elif(result == 5):
            #Save and return
            self.save()
            return None
        elif((result == DELETE)or(result == QUIT)):
            raise Exception("Quitting menu for DELETE")
        return self.edit_options(selected=result)

    def change_value(self, current_value, values_list):
        if(current_value in values_list):
            index = values_list.index(current_value)
            index += 1 #Changin the index
            if(index == len(values_list)):
                index = 0 #Rotating back to the beginning if the end is reached
            return values_list[index]
        return current_value #Should not never happen
