#author: n01
"""
The map manager is in charge of loading, managing and rendering the map
based on the information that recives during a frame
P.S.
In this case a frame is the lass of time where it is printed an (old) rappresentation of the game
"""
from local_imports import *
from misc import *
from Player import *

class MapManager(object):

    def __init__(self, map_name):
        """
        @map_name: is the filename to the map that must be loaded (extensions are discarted)
        """
        self.map_name = map_name.split(".")[0] #Removing all possible extensions
        self.vmap = None #Virtual map, i.e. the skeleton map before the rendering part
        self.map = None #Map to be returned when needed to be rendered
        self.buffer_line1 = None #First buffer line - reserved for player turn display
        self.buffer_line2 = None #Second buffer line
        self.buffer_line3 = None #Second buffer line
        self.id = None #Map Identifiers (ID for short), they are used to manage the logic of the virtual map
        self.bonus = [] #Continental bonus: bonus given when a player owns an entire continent
        self.visibility = True #VIsibility of the map, concealed during an attack or strategic movement
        #Country ids
        self.current_country = None #The current country is the country that the player is considering
        self.selected_country= None #Country selected to the player to perform actions
        self.target_country = None #A country performing an action must have a nearby (ally or enemy) target
        #Loading map related resources
        self.load_map()
        self.load_id()
        self.load_bonus() #This is optional

    def render_opt(self, map_line):
        """
        Splits a renderable map line into 'intervals'.
        In this way the coloring process, that comes with each frame renderization, is made easier
        breacuse instead of coloring letter per letter the program colors interval per interval
        """
        opt_map_line = [] #The result matrix
        map_line = list(map_line) #Split the string in a characters list
        interval_id = map_line[0] #Interval identity: the character that defines the interval
        interval = [] #Interval list to append to opt_map_line
        for i in map_line:
            if(i == interval_id):
                #Add character to interval
                interval.append(i)
            else:
                #New character found
                opt_map_line.append("".join(interval)) #Update the opt_map_line
                interval = [] #Clear the interval variable
                interval_id = i #Change the interval_id
                interval.append(i) #Don't forget to append the character, or you're losing it
        opt_map_line.append("".join(interval)) #Last interval to add
        return opt_map_line


    def load_map(self):
        """
        Loads the map resource and returns a optimized renderable map
        """
        with open(MAP_FOLDER + self.map_name + ".map", "r") as file:
            map_contents = file.read()
        map_contents = map_contents.split("\n")
        # if(map_contents[len(map_contents)-1] == ''):
        #     #Newline detected, remove it
        #     map_contents = map_contents[:len(map_contents)-1]
        map_contents = resolve_newline(map_contents)
        results = [self.render_opt(x) for x in map_contents] #Map rendering optimization
        self.vmap = results
        # return map_contents

    def load_id(self):
        """
        Loads the map identifiers file (.id) that contains data about the map.
        identifiers file spec: the file MUST have the same name of the map
        the extension differs from .map to .id and the location folder is the same.
        Please keep in mind this, if you're planning to create a new map
        """
        with open(MAP_FOLDER + self.map_name + ".id", "r") as file:
            id_content = file.read()
        id_content = id_content.split("\n")
        id_content = resolve_newline(id_content)
        id = []
        for i in id_content:
            line = i.split(":")
            if(len(line) != 4):
                raise Exception("ID file malformed")
            try:
                state_name = line[0]
                state_id = line[1]
                state_borders = [int(x) for x in line[2].split(",")]
                renderable_id = line[3]
                id.append({NAME: state_name, ID: state_id, BORDERS: state_borders, OWNER: NO_ONE, TROUPS: 0, RENDERABLE_ID: renderable_id}) #TODO: see if you can format it better
            except:
                raise Exception("ID content parsing exception")
        #Checking the mimnimum number of nations for generating a map
        if(len(id)<6):
            raise Exception("Insufficient nations in map, at least 6 nations are required")
        #ID is correctly generated
        self.id = id

    def load_bonus(self):
        """
        This function checks if the bonus files exists in the folder and then
        updates the bonus attribute
        """
        try:
            with open(MAP_FOLDER + self.map_name + ".bonus", "r") as file:
                bonus_contents = file.read()
            bonus_contents = bonus_contents.split("\n")
            bonus_contents = resolve_newline(bonus_contents)
            for continent in bonus_contents:
                (countries, bonus) = continent.split(":")
                countries = [int(x) for x in countries.split(",")]
                bonus = int(bonus)
                if(bonus<0):
                    raise Exception("Negatives bonuses are not allowed")
                self.bonus.append({CONTINENT: countries, BONUS: bonus})
        except:
            self.bonus = [] #No bonuses file avaiable or malformed file, bonuses are disabled

    def render(self):
        """
        The idea is to create from the virtual map (the skeleton of the map)
        the actual frame-renderable map to be printed on screen based on the informations
        about the players that the map manager receives
        The constructed self.map attribute is then returned to be printed by the caller
        or an other function
        """
        #DEBUG render v2
        # lines = ["".join(x) for x in self.vmap]
        troups_text = [self.map_str(x[TROUPS]) for x in self.id] #Select all troups based on state order
        troups = [colored(troups_text[x], self.id[x][OWNER]) for x in range(len(troups_text))] #Coloring the numbers for better reading
        tmp_grid = []
        for line in self.vmap:
            tmp_line = []
            for interval in line:
                #Intervals are guaranteed to have at least one character
                if(not(interval[0] in IGNORABLE_CHARACTERS)):
                    (owner_color, renderable_id, country_id) = self.resolve_id(interval[0])
                    attribute = self.map_style(country_id) #The style changes if the country is selected or not
                    tmp_interval = colored(renderable_id*len(interval), owner_color, attrs=attribute)
                else:
                    if(self.visibility):
                        tmp_interval = interval
                    else:
                        tmp_interval = colored(" "*len(interval), WHITE, attrs=CONCEALED)
                tmp_line.append(tmp_interval)
            tmp_grid.append(tmp_line)

        ###
        #Putting the pieces together
        lines = ["".join(x) for x in tmp_grid] #Joining the intervals
        self.map = "\n".join(lines) #Joining the lines
        # numbers = [colored(self.map_str(x), "red") for x in range(0, 42)]
        self.map = self.map.format(*troups) #Very cool python feature, it has nothing to do with pointers :)
        return self.map

    def map_str(self, number):
        """
        The map_str function returns the string rappresentation of the given number
        padding the result to two characters wide space
        """
        result = "  "
        # if(number == None):
        #     return result #Yes, that should work ~ EDIT: It doesn't, it break things
        if(number<=0):
            return result #Negative values are not allowed
        elif(number<=9):
            return " " + str(number) #Single digits numbers must be padded
        elif(number<=99):
            return str(number) #Double digits numbers have no problems
        else:
            return "++" #Too much troops cause an 'innumerable' status

    def resolve_id(self, id):
        """
        Given a map identifier the index of the country on the self.id list is found
        for then returning a touple with these two values:
            owner of the country, also works as color
            @renderable_id: the character used in the rappresentation, more appealing to the eye
            @index: The country unique identifier
        """
        ids = [x[ID] for x in self.id]
        index = None #Visibility purposes
        try:
            index = ids.index(id)
        except:
            raise Exception("Conflict between the ID data and map data")
        return (self.id[index][OWNER], self.id[index][RENDERABLE_ID], id) #The owners are the name of the avaiable colors

    def map_style(self, country_id):
        """
        Different styles can be applied to the colors via the attrs named param
        in the colored function.
        This function checks if the piece of data simbolyzing a country
        (rappresented by the country_id number) must be changed in style and returns it.
        The default style is NO_ATTRS
        """
        if(country_id == self.current_country):
            return BLINK
        elif(country_id == self.selected_country):
            return BOLD
        elif(country_id == self.target_country):
            return DARK #Maybe a BLINK is better
        else:
            if(self.visibility):
                return NO_ATTRS #Default case
            else:
                return CONCEALED

    def show_frame(self):
        """
        This function prints the rendered map with the two buffer lines (A game frame)
        Nothing special
        """
        self.render() #To show a rendered map, first render it ._.
        clear() #Clearing the screen
        print(self.map)
        print(self.buffer_line1)
        print(self.buffer_line2)
        print(self.buffer_line3)

    # def update_id(self, id):
    #     """
    #     This function is critical to the management of the Map but I must
    #     let the control logic to be checked and performed in the GameManager
    #     class, so do not use MapManagers outside that class if you don't
    #     know what you're doing
    #     """
    #     if((type(self.id) == type(id))and(len(self.id) == len(id))): #Some superficial checks, the logic checks are performed by the caller, not the callee
    #         self.id = id

    # def update_id(self, player):
    #     """
    #     This function updates the status of the countries, who ownes them,
    #     how many troups there are, etc...
    #     """
    #     if(type(player) == Player):
    #         countries = player.get_countries()
    #         troups = player.get_troups()
    #         for i in range(len(countries)):
    #             self.id[countries[i]][OWNER] = player.color
    #             self.id[countries[i]][TROUPS] = troups[i]

    def get_countries_by_owner(self, owner):
        if((owner in COLORS)and(owner != NO_ONE)):
            return [country for country in self.id if country[OWNER] == owner] #Seems like a database backend method

    def toggle_visibility(self):
        self.visibility = not(self.visibility)
