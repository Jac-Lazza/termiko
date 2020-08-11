#author: n01
"""
The class GameManager manages an instance of the game, contemplating all players,
the map and that the rules of the game are respected
"""
from local_imports import *
from MapManager import *
from misc import *
from Player import *
from OptionManager import *

class GameManager(object):

    def __init__(self, optionManager):
        """
        Notes: After a choose method (those methods that have a chance of spawining a menu) give always a clear() call
        """
        self.options = optionManager #This should copy the pointer if I'm correct
        self.players_names = [] #Players name, this attribute is just for comfort
        self.players = None #Players instances
        self.id = None #GameManager has its own copy of the map id
        self.map = None #The map of the game
        self.current_turn = 0 #The list index of the self.players, the first on the list starts
        # self.current_country = 0 #The current country list index, always starting from the beginning
        self.default_armies()
        self.choose_armies()
        clear()
        #Armies are chosen creating new players
        # self.players_names.sort() #Could leave like thtat
        self.players = [Player(x, self.options.options[AVAIABLE_TROUPS]) for x in self.players_names]
        random.shuffle(self.players) #Randomizing the order of the players
        #Choosing the map
        mapname = self.choose_map()
        clear()
        self.map = MapManager(mapname)
        # self.id = list(self.map.id)
        self.id = self.map.id #The two id attributes are now entagled with one pointer
        #Now that we have a map, territories must be divided between the players
        self.init_countries()

    def default_armies(self):
        """
        This function establishes the minimum number of troups for playing the game
        and als defines their colors.
        It can be considered as a choose_armies init function
        """
        self.players_names.append(RED)
        self.players_names.append(BLUE)

    def choose_armies(self, selected=0):
        """
        This function lets you choose the number and colors of your armies.
        It is required that a minimum of two players must play the game, the color
        is not important
        """
        #Adjusting the rendering aspects of the text
        armies_text = list(self.options.translation[ARMIES].values()) #Getting the names of the armies
        armies_menu_text = ["[ ] " + x for x in armies_text] #Adding [ ] to each entry
        for i in self.players_names: #Rendering selected armies
            id = COLORS.index(i)
            armies_menu_text[id] = "[*] " + armies_text[id]
        if(len(self.players_names)>=2):
            armies_menu_text.append(self.options.translation[CONFIRM]) #Adding the confirm entry
        #Spawning the menu
        #BUG: There is some problem with the optional_text formatting, I had to add " "*12 to center it manually
        selected = menu(armies_menu_text, selected=selected, optional_text=self.options.translation[ARMIES_SELECTION])
        if(selected == 6):
            return None #Choice confirmed
        elif(selected == DELETE):
            raise Exception("Quitting menu for DELETE")
        #Modify the self.players_names list
        color = COLORS[selected]
        if(color in self.players_names):
            #Element to remove
            self.players_names.remove(color)
        else:
            #Element to add
            self.players_names.append(color)
        return self.choose_armies(selected=selected)

    def choose_map(self):
        """
        This function is used to choose the game map.
        Maps are automatically gathered from the MAP_FOLDER and ends with the .map file extension
        If no maps are found an exception is raised (and the game crashes, because I'm too lazy to manage exceptions ;) )
        If only one map is found (The default one is the classic world_map) then it is selected without asking
        If multiple maps are found, a menu is spawned and the player can choose wich map to play
        I recall that a map is composed of two main files: the .map and .id files. this function only check the existence of
        the .map file, but without the .id the game crashes with a custom exception as it is supposed to
        """
        map_folder_contents = os.listdir(MAP_FOLDER)
        avaiable_maps = [x.split(".")[0] for x in map_folder_contents if x.endswith(".map")] #Filtering only maps files
        if(len(avaiable_maps) == 0):
            raise Exception("Error, no maps provided in the " + MAP_FOLDER + " folder")
        elif(len(avaiable_maps) == 1):
            #Only one map, no time left to choose
            return avaiable_maps[0]
        else:
            #Multiple maps avaiable, choose one!
            result = menu(avaiable_maps, optional_text=self.options.translation[MAP_SELECTION])
            if(result == DELETE):
                raise Exception("Quitting menu for DELETE")
            return avaiable_maps[result]

    def init_countries(self):
        """
        When the game starts, a predefined number of countries is given to each player.
        In this version the game that number is calculated based of the number of avaiable countries avaiable
        """
        countries_number = len(self.id)
        initial_number_countries = countries_number//6 #6 is the maximum amount of players
        avaiable_countries_index = [x for x in range(countries_number)] #Saving the id indexes of the countries
        for player in self.players:
            #For each player give an initial_number_countries to own and modify the id list related data
            for _ in range(initial_number_countries):
                index = random.randint(0, len(avaiable_countries_index)-1)
                id = avaiable_countries_index[index] #Getting the id index to then access the list and modify it
                avaiable_countries_index.pop(index) #Removing the chosen index
                self.id[id][OWNER] = player.color
                self.id[id][TROUPS] = 1 #At least one troup in a territory to claim it

    def next_turn(self):
        """
        This function simply increments the self.current_turn variable by keeping
        it into the self.players restraints
        """
        self.current_turn = (self.current_turn+1)%len(self.players) #So we get always a value between 0 and len(self.players)-1

    # def next_country(self, country_list):
    #     """
    #     As above, so below
    #     """
    #     self.current_country = (self.current_country+1)%len(country_list) #Lets see if this method lasts

    def initial_turn(self):
        """
        Play the initial turn for all players.
        During this turn players can only manage initial troup numbers,
        they cannot attack other countries or make strategical movements
        """
        for player in self.players:
            countries = self.map.get_countries_by_owner(player.color)
            self.manage_troups(player, countries)

    def play_turn(self):
        """
        This is the main method where all the game action is applied
        It must be called for each turn, and each turn has three phases
        1) Bonus Calculation (Easy thing to do, need to check if bonuses are avaiable or not though)
        2) Troups management
        3) Countries attack and strategic movement
        """
        ### PART 1
        player = self.players[self.current_turn] #Saving the player for now
        countries = self.map.get_countries_by_owner(player.color) #Fetching owned countries
        if(countries == []): #A player that has no countries is a dead player
            #Eliminated players should be removed from the list, this is a security check to avoid complications
            self.next_turn()
            return None #Premature end of the turn
        troups_bonus = len(countries)//3 #3 is another magic number (found in the original game btw), I know, maybe one day I'll refactor
        player.increase_avaiable_troups(troups_bonus)
        if(self.options.options[CONTINENTAL_BONUS] == 1):
            #Continental bonus is enabled
            #Checking if the bonus can be applied
            # countries_id = [x[ID] for x in countries] #Extracting data just one time #BUGFIX: The id is not the same thing as the index, let's change and use the index
            countries_indexes = self.resolve_countries(countries)
            for continent in self.map.bonus:
                for country in continent[CONTINENT]:
                    if(not(country in countries_indexes)):
                        break
                else:
                    player.increase_avaiable_troups(continent[BONUS]) #Adding the continental bonus
            #This will do, for now

        ### PART 2
        country_index = self.manage_troups(player, countries)

        ### PART 3
        # country_index = 0 #The structure is similiar to the one found in self.manage_troups()
        while(True):
            countries = self.map.get_countries_by_owner(player.color)
            self.map.current_country = countries[country_index][ID]
            self.map.buffer_line1 = colored(buffer_line_pad(self.options.translation[PLAYER]), MAGENTA) + colored(self.options.translation[ARMIES][player.color], player.color) + CHESS_BLOCK + colored(countries[country_index][NAME], CYAN)
            self.map.buffer_line2 = colored(buffer_line_pad(self.options.translation[DEPLOYED_TROUPS]), MAGENTA) + colored(BULLET_BLOCK*min(countries[country_index][TROUPS], get_avaiable_columns()), player.color)
            self.map.buffer_line3 = ""
            self.map.show_frame()
            key_pressed = readArrow()
            if(key_pressed == RIGHT):
                country_index = (country_index+1)%len(countries)
            elif(key_pressed == LEFT):
                country_index = country_index-1 if (country_index-1)>=0 else len(countries)-1
            elif(key_pressed == ENTER):
                #Country selected, ready for attack or strategic movement
                if(countries[country_index][TROUPS]>1): #Can't move a thing or attack if the avaiable troups in that country is lower or equal to one
                    is_strategic_movement = self.move_troups(countries[country_index])
                    if(is_strategic_movement):
                        break #End of the turn if it was a strategic movement
                else:
                    pass #Ignore, do nothing
            elif(key_pressed == DELETE):
                break #Pass the turn to someone else
            else:
                pass #Do nothing
        self.next_turn()

    def move_troups(self, selected_country):
        """
        This function makes the necessary preparations to arrange a troup movement,
        either a strategic one or an attack.
        Returns True if the movement was a strategic one (this mean an end of the turn)
        """
        borders = selected_country[BORDERS] #Getting the nearest countries to the selected one
        border_index = 0 #Same as country_index when it is first initialized
        self.map.current_country = None #Cleaning this status variable, it is not needed
        while(True):
            border_country = self.id[borders[border_index]] #It seems complicated, but borders is just a list of indexes for the self.id list
            self.map.selected_country = selected_country[ID]
            self.map.target_country = border_country[ID]
            #Changing the buffer_lines
            self.map.buffer_line1 = colored(buffer_line_pad(self.options.translation[TROUPS_MOVEMENT]), MAGENTA) + colored(selected_country[NAME], selected_country[OWNER]) + CHESS_BLOCK + colored(border_country[NAME], border_country[OWNER])
            self.map.buffer_line2 = colored(buffer_line_pad(self.options.translation[DEPLOYED_TROUPS]), selected_country[OWNER]) + colored(BULLET_BLOCK*min(selected_country[TROUPS], get_avaiable_columns()), selected_country[OWNER])
            if(selected_country[OWNER] != border_country[OWNER]):
                buffer_line_text = buffer_line_pad(self.options.translation[ENEMY_TROUPS])
            else:
                buffer_line_text = buffer_line_pad(self.options.translation[ALLIED_TROUPS])
            self.map.buffer_line3 = colored(buffer_line_text, border_country[OWNER]) + colored(BULLET_BLOCK*min(border_country[TROUPS], get_avaiable_columns()), border_country[OWNER])
            self.map.show_frame()
            key_pressed = readArrow()
            if(key_pressed == RIGHT):
                border_index = (border_index+1)%len(borders)
            elif(key_pressed == LEFT):
                border_index = border_index-1 if (border_index-1)>=0 else len(borders)-1
            elif(key_pressed == ENTER):
                attacker_player = selected_country[OWNER]
                defender_player = border_country[OWNER]
                if((attacker_player == defender_player)or(defender_player == NO_ONE)):
                    #This counts as a strategic movement
                    try:
                        self.strategic_movement(selected_country, border_country)
                        self.map.selected_country = None
                        self.map.target_country = None
                        return True
                    except:
                        pass #Movement canceled
                else:
                    #This is an attack against some other player
                    try:
                        self.attack(selected_country, border_country)
                        self.map.selected_country = None
                        self.map.target_country = None
                        return False
                    except:
                        pass #Attack canceled
            elif(key_pressed == DELETE):
                #Aborting the operation, restoring map status variables
                self.map.current_country = selected_country[ID]
                self.map.selected_country = None
                self.map.target_country = None
                return False #Return the control, not the end of the turn
            else:
                pass #Do nothing
        self.next_turn() #End of the turn

    def strategic_movement(self, source, destination, number_troups_to_move=0, unblockable=False):
        """
        This is the strategic_movement function.
        A strategic movement is done when:
        You move troups to an unconquered country
        You move troups to an ally
        You move troups to a conquered country
        The last case is the only one that doesn't count as end of the turn and it is called by the
        attack function
        EDIT: Need to think about the number_troups_to_move there, the minimum number is
        one, of corse, but it's counterintuitive the number of troups moved effectively
        against the ones you select. To adjust later, this is user experience stuff
        and I'm still working with the bones and skin of this thing
        """
        self.map.toggle_visibility()
        avaiable_troups = source[TROUPS]-number_troups_to_move
        min_troups = number_troups_to_move
        while(True):
            #Rendering part
            self.map.buffer_line1 = colored(buffer_line_pad(self.options.translation[OPTIONS][AVAIABLE_TROUPS].upper()), MAGENTA) + colored(BULLET_BLOCK*min(avaiable_troups, get_avaiable_columns()), source[OWNER])
            self.map.buffer_line2 = colored(buffer_line_pad(self.options.translation[TROUPS_TO_MOVE]), MAGENTA) + colored(BULLET_BLOCK*min(number_troups_to_move, get_avaiable_columns()), source[OWNER])
            self.map.buffer_line3 = ""
            self.map.show_frame()
            #Reading the key
            key_pressed = readArrow()
            if(key_pressed == RIGHT):
                if(avaiable_troups>1):
                    number_troups_to_move += 1
                    avaiable_troups -= 1
            elif(key_pressed == LEFT):
                if(number_troups_to_move>min_troups):
                    number_troups_to_move -= 1
                    avaiable_troups += 1
            elif(key_pressed == ENTER):
                if(number_troups_to_move>0):
                    break
            elif(key_pressed == DELETE):
                if(unblockable):
                    #Using default numbers
                    number_troups_to_move = 1
                    break
                else:
                    #Function aborted
                    self.map.toggle_visibility()
                    raise Exception("Function aborted")
            else:
                pass #Do nothing
        #Confirm last operations
        source[TROUPS] -= number_troups_to_move
        destination[TROUPS] += number_troups_to_move
        destination[OWNER] = source[OWNER]
        self.map.toggle_visibility()
        self.update_id_attribute([source, destination])

    def attack(self, attacker, defender):
        self.map.toggle_visibility()
        #Variable space
        modality = True #True => attack preparation ~ False => Defence preparation
        attacker_troups = 1
        defender_troups = 1
        attacker_avaiable_troups = attacker[TROUPS]-1
        defender_avaiable_troups = defender[TROUPS]-1
        ###
        while(True):
            block = "█"*(get_avaiable_columns()*10//100) + " "
            if(modality):
                attacker_arrow = "|> "
                defender_arrow = "   "
            else:
                attacker_arrow = "   "
                defender_arrow = "|> "
            self.map.buffer_line1 = colored(attacker_arrow, MAGENTA, attrs=BLINK) + colored(buffer_line_pad(self.options.translation[ATTACK_PREPARATION]), attacker[OWNER]) + colored(block*attacker_troups, attacker[OWNER])
            self.map.buffer_line2 = ""
            self.map.buffer_line3 = colored(defender_arrow, MAGENTA, attrs=BLINK) + colored(buffer_line_pad(self.options.translation[DEFENCE_PREPARATION]), defender[OWNER]) + colored(block*defender_troups, defender[OWNER])
            self.map.show_frame()
            key_pressed = readArrow()
            if(key_pressed == RIGHT):
                if(modality):
                    if((attacker_avaiable_troups>1)and(attacker_troups<3)):
                        attacker_troups += 1
                        attacker_avaiable_troups -= 1
                else:
                    if((defender_avaiable_troups>0)and(defender_troups<3)):
                        defender_troups += 1
                        defender_avaiable_troups -= 1
            elif(key_pressed == LEFT):
                if(modality):
                    if(attacker_troups>1):
                        attacker_troups -= 1
                        attacker_avaiable_troups += 1
                else:
                    if(defender_troups>1):
                        defender_troups -= 1
                        defender_avaiable_troups += 1
            elif(key_pressed == ENTER):
                if(modality):
                    modality = False #Switching to defence mode
                else:
                    break #Exiting the while loop and Executing the attack
            elif(key_pressed == DELETE):
                if(modality):
                    self.map.toggle_visibility()
                    raise Exception("Attack aborted") #The attack can be canceled by the attacker player
                else:
                    pass #Ignore it, the defender cannot cancel the attack by any means
            else:
                pass #Ignore other keys pressings
        #Processing the attack
        attacker_rolls = [random.randint(1,6) for _ in range(attacker_troups)]
        defender_rolls = [random.randint(1,6) for _ in range(defender_troups)]
        attacker_rolls.sort(reverse=True)
        defender_rolls.sort(reverse=True)
        max_roll_length = max(len(attacker_rolls), len(defender_rolls))
        self.map.buffer_line1 = colored(buffer_line_pad(self.options.translation[DEPLOYED_TROUPS]), attacker[OWNER])
        self.map.buffer_line2 = ""
        self.map.buffer_line3 = colored(buffer_line_pad(self.options.translation[ENEMY_TROUPS]), defender[OWNER])
        pad_number = get_avaiable_columns()*10//100
        attacker_number = None #For visibility
        defender_number = None
        removed_attacker_troups = 0
        removed_defender_troups = 0
        for i in range(max_roll_length):
            #Extracting attacker numbers
            try:
                attacker_number = attacker_rolls[i]
            except:
                attacker_number = ""
            #Extracting defender numberss
            try:
                defender_number = defender_rolls[i]
            except:
                defender_number = ""
            #Comparing them
            if((attacker_number == "")or(defender_number == "")):
                #No need to count it on the removal of troups
                attacker_text = colored(str(attacker_number).center(pad_number), attacker[OWNER])
                defender_text = colored(str(defender_number).center(pad_number), defender[OWNER])
            elif(attacker_number<=defender_number): #Need to check the result
                attacker_text = colored(str(attacker_number).center(pad_number), attacker[OWNER])
                defender_text = colored(str(defender_number).center(pad_number), defender[OWNER], "on_" + WHITE)
                removed_attacker_troups += 1
            else:
                #attacker_number>defender_number
                attacker_text = colored(str(attacker_number).center(pad_number), attacker[OWNER], "on_" + WHITE)
                defender_text = colored(str(defender_number).center(pad_number), defender[OWNER])
                removed_defender_troups += 1
            #Rendering the thing
            self.map.buffer_line1 += attacker_text
            self.map.buffer_line3 += defender_text
            self.map.show_frame()
            time.sleep(0.5)
        #End of attack, returning control over the player
        self.map.toggle_visibility()
        attacker[TROUPS] -= removed_attacker_troups
        defender[TROUPS] -= removed_defender_troups
        defendant = defender[OWNER] #Saving the owner, in case the method belows change things that I don't want (I honestly don't remember)
        if(defender[TROUPS]<=0):
            #Territory conquered, adding it
            self.strategic_movement(attacker, defender, (len(attacker_rolls)-removed_attacker_troups), unblockable=True)
        else:
            self.update_id_attribute([attacker, defender])
        #Cleaning the map a bit
        self.map.selected_county = None
        self.map.target_country = None
        #Checking if the defeated player can still play the game
        enemy_countries = self.map.get_countries_by_owner(defendant)
        if(enemy_countries == []):
            #Enemy defeated
            index = self.players_names.index(defendant)
            self.players_names.pop(index)
            self.players.pop(index)


    def manage_troups(self, player, countries):
        """
        This function manages avaiable troups owned by a player
        P.S. This is one of the biggest bastards I have to write I think...
        Let's hope all well ends well
        """
        country_index = 0 #Always start from the beginning of the list
        # tmp_countries = list(countries)
        while(True):
            self.map.current_country = countries[country_index][ID] #Selecting the country with her own id
            self.map.buffer_line1 = colored(buffer_line_pad(self.options.translation[PLAYER]), MAGENTA) + colored(self.options.translation[ARMIES][player.color], player.color) + CHESS_BLOCK + colored(countries[country_index][NAME], CYAN)
            self.map.buffer_line2 = colored(buffer_line_pad(self.options.translation[AVAIABLE_TROUPS]), MAGENTA) + BULLET_BLOCK*min(player.avaiable_troups, get_avaiable_columns())
            self.map.buffer_line3 = colored(buffer_line_pad(self.options.translation[DEPLOYED_TROUPS]), MAGENTA) + colored(BULLET_BLOCK*min(countries[country_index][TROUPS], get_avaiable_columns()), player.color)
            self.map.show_frame()
            #Ok control wise it's quite rigid, but I had to make some choice to make my life easier
            key_pressed = readArrow()
            if(key_pressed == RIGHT):
                country_index = (country_index+1)%len(countries)
            elif(key_pressed == LEFT):
                country_index = country_index-1 if (country_index-1)>=0 else len(countries)-1
            elif(key_pressed == ENTER):
                try:
                    player.decrease_avaiable_troups(1)
                    countries[country_index][TROUPS] += 1
                except:
                    #Avaiable troups are finished, end of managing
                    self.update_id_attribute(countries)
                    return country_index
            elif(key_pressed == DELETE):
                self.update_id_attribute(countries)
                return country_index
            else:
                pass #Do nothing

    def update_id_attribute(self, updated_content):
        """
        This method is used to update both the local and the MapManager id structure
        """
        for element in updated_content:
            for i in range(len(self.id)):
                if(element[ID] == self.id[i][ID]):
                    #Element to update
                    self.id[i] = element
        #Once updated the local id, update the map
        self.map.id = self.id #This could be not necessary, thanks to pointers

    def resolve_countries(self, countries):
        """
        This function resolves a list of countries into the a list of self.d indexes.
        This method could have been writte both in the GameManager and the the MapManager with
        no problems. It's a personal choice to give more power to the GameManager,
        the MapManager should use its stuctures only for rendering things, not
        manage them
        """
        country_indexes = []
        for country in countries:
            try:
                index = self.id.index(country)
                #Country found, add it to the list
                country_indexes.append(index)
            except:
                pass
        return country_indexes #Return the results
