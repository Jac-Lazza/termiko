#author: n01
"""
The RuleManager, as the name suggestes, manages the rules of the game,
it gets the current language setting and does a job similiar to the one done
by the OptionManager when searching for translations
"""
from misc import *
from local_imports import *

class RulesManager(object):

    def __init__(self, lang):
        if(lang in LANGS):
            self.lang = lang
        else:
            raise Exception("Invalid language") #This should never be raised
        self.screens = [] #The rules screens to be passed one by one
        self.screens_index = 0 #The current screen of the "carousel"
        self.load_rules()

    def load_rules(self):
        """
        Loads the game rules with the current translation.
        Game rules are divided in screens and are found in the LANG_PATH/LANG dir
        """
        lang_dirbase = LANG_FOLDER + self.lang + "/"
        files = os.listdir(lang_dirbase)
        screens_files = [x for x in files if x.endswith(".screen")] #Filtering the files
        screens_files.sort() #The file names must be sorted, not the file contents, it was a nice bug
        self.screens = []
        for i in screens_files:
            with open(lang_dirbase + i, "r") as file:
                content = file.read()
            self.screens.append(content) #Updating the screens attribute
        # self.screens.sort() #BUGFIX: (this description is valid for above) Sorting filenames, it's a quick solution, but you have constraints on how to name them
        #Although I don't think to have more than ten screens of rules, so this should be no problem

    def parse_rules_text(self, content):
        """
        This function parses the text found in the .screen files.
        It's a very simple and dumb parser so don't abuse it and check the
        opening and closing of the tags.
        For now the tags are:
         -) Nothing to make the text MAGENTA
         -) *something* to make the text UPPERCASE, CYAN, BOLD (use it for titles)
        """
        content = content.split("\n")
        content = resolve_newline(content)
        screen = []
        title = True
        for row in content:
            pieces = row.split("*")
            colored_pieces = []
            mode = True
            for piece in pieces:
                if(mode):
                    #Normal mode
                    colored_pieces.append(colored(piece, MAGENTA))
                else:
                    #Highlighted mode
                    colored_pieces.append(colored(piece.upper(), CYAN, attrs=BOLD))
                mode = not(mode) #Toggling the mode
            parsed_row = "".join(colored_pieces) #Joining the pieces to form a row
            if(title):
                parsed_row += colored(" " + str(self.screens_index+1) + "/" + str(len(self.screens)), CYAN, attrs=BOLD) #Adding number of screens, to give an idea of how much to read
                parsed_row = parsed_row.center(get_avaiable_columns()) #This is the title of the screen
                title = False
            else:
                initial_padding = " "*(get_avaiable_columns()*30//100)
                parsed_row = initial_padding + parsed_row
            screen.append(parsed_row)
        return screen #The result should be parsed immediately by the show_screen function

    # def show_screen(self, screen):
    #     """
    #     This function takes a list of centered and colored strings
    #     and prints them. Very simple, what could possible go wrong? (Graphical TOCTOU?)
    #     """
    #     for i in screen:
    #         print(i) #Ok, maybe I thought this function could do more

    def show_rules(self):
        self.screens_index = 0
        if(len(self.screens) == 0):
            #End prematurely, no rules loaded (maybe they are not avaiable)
            return None
        while(True):
            screen = self.parse_rules_text(self.screens[self.screens_index]) #Get the content parsed
            #Showing the screen
            clear()
            for line in screen:
                print(line)
            ####
            direction = readArrow()
            if((direction == RIGHT)or(direction == ENTER)):
                if(self.screens_index == (len(self.screens)-1)):
                    break #End of the show
                self.screens_index += 1 #Nex screen
            elif(direction == LEFT):
                if(self.screens_index>0):
                    self.screens_index -= 1
            elif((direction == DELETE)or(direction == QUIT)):
                break #Doesn't want to read the rules anymore
            else:
                pass #Do nothing
