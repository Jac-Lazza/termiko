#author: n01
import messages
from local_imports import *
from misc import *
from MapManager import *
from OptionManager import *
from GameManager import *

options = OptionManager()
result = 0 #Selecting the first item on the menu list
while(True):
    menu_text = list(options.translation[MAIN_MENU].values())
    result = messages.main_menu(menu_text, result)
    win_message = ""
    winner = ""
    if(result == 0): #Local match
        try:
            game = GameManager(options) #Creating a new game
            gamemode = options.options[GAMEMODE] #Getting the gamemode
            turn_limit = options.options[TURN_LIMIT] #Getting the turn limit
            if(turn_limit == "∞"):
                turn_limit = True
            turn_number = 1 #Initializing the current turn number
            game.initial_turn() #First turn for everyone
            while(turn_number<=turn_limit): #Funy thing, somethingsomething<True gives always true!
                game.play_turn()
                if(gamemode == 0): #World domination
                    possible_winner = game.id[0][OWNER]
                    for owner in [x[OWNER] for x in game.id]:
                        if(possible_winner!=owner):
                            break #Objective not satisfaied
                    else:
                        #Objective satisfied, possible_winner is the winner
                        win_message = options.translation[WIN_MESSAGES][WIN_WORLD_DOMINATION]
                        winner = colored(options.translation[ARMIES][possible_winner], possible_winner)
                elif(gamemode == 1): #Enemy elimination
                    if(len(game.players) == 1):
                        #All enemies defeated
                        winning_player = game.players[0].color
                        win_message = options.translation[WIN_MESSAGES][WIN_ENEMY_ANNIHILATION]
                        winner = colored(options.translation[ARMIES][winning_player], winning_player)
                else:
                    pass #Do nothing
                turn_number += 1
            else:
                #Turn limit obtained, end the game with a neutral message
                #Counting points for each player
                final_score = []
                for player in game.players_names:
                    player_countries = game.map.get_countries_by_owner(player)
                    score = 0
                    for country in player_countries:
                        points = len(country[BORDERS])
                        score += points
                    final_score.append(score)
                #Now we have all the final scores, we get the maximum one
                max_score = max(final_score)
                if(final_score.count(max_score) > 1):
                    #We get a DRAW, more players have the same score
                    win_message = options.translation[WIN_MESSAGES][WIN_DRAW]
                    winners_count = final_score.count(max_score)
                    winner = " ~~~ "
                    for _ in range(winners_count):
                        index = final_score.index(max_score)
                        final_score[index] = None #Deleting used max scores
                        winner += colored(options.translation[ARMIES][game.players_names[index]], game.players_names[index]) + " ~~~ "#This should add all the winners to the list
                else:
                    #We get the winner for turn limit
                    winner_index = final_score.index(max_score)
                    winner_name = game.players_names[winner_index]
                    win_message = options.translation[WIN_MESSAGES][WIN_TURN_LIMIT]
                    winner = colored(options.translation[ARMIES][winner_name], winner_name)
                    pass
            #Prepearing the map to be displayed
            #Cleaning cursor countries
            game.map.current_country = None
            game.map.selected_country = None
            game.map.target_country = None
            #Prepearing buffer lines
            game.map.buffer_line1 = colored(win_message.center(get_avaiable_columns()), MAGENTA)
            game.map.buffer_line2 = winner.center(get_avaiable_columns())
            game.map.buffer_line3 = colored(options.translation[PRESS_CONTINUE].center(get_avaiable_columns()), CYAN)
            #Showing the frame one last time
            game.map.show_frame()
            input() #Just waiting that ENTER is pressed, then we return to the main menu
        except:
            pass #Handling all possible exceptions in GameManager
    elif(result == 1): #Network match
        clear()
        print(colored("Still a work in progress!", MAGENTA)) #TODO
        input("~~~ press ENTER to return to the main menu ~~~")
    elif(result == 2): #Game rules
        try:
            options.rules.show_rules()
        except:
            pass #Do nothing, probably it was a DELETE
    elif(result == 3): #Options
        try:
            options.edit_options()
        except:
            pass
    elif(result == 4): #Exiting the game
        break
    elif(result == DELETE):
        result = 0 #Do nothing if DELETE is pressed and reset the result variable to the beginning
    else:
        sys.exit(1)
#Maybe add some end message here
# clear()
sys.exit(0)
