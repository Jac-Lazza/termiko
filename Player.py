#author: n01
"""
The player manager manages player status, data and other related informations
It's important that the PlayerManager and the MapManager communicate through the
inner game logic
"""
from local_imports import *

class Player(object):

    def __init__(self, color, initial_troups):
        if(color in COLORS):
            self.color = color
        else:
            raise Exception("Not a valid color for an army")
        self.avaiable_troups =  initial_troups #Default value for troups, maybe configurable through the options (need OptionManager)
        # self.owned = [] #List of owned states, empty for starters

    # def get_countries(self):
    #     return [x[0] for x in self.owned]
    #
    # def get_troups(self):
    #     return [x[1] for x in self.owned]
    #
    # def increase_avaiable_troups(self, number):
    #     if(number>=0):
    #         self.troups += number
    #
    # def decrease_avaiable_troups(self, number):
    #     if((number>=0)and(number<=self.avaiable_troups)):
    #         self.avaiable_troups -= number
    #         return number

    def increase_avaiable_troups(self, value):
        if(value>=0):
            self.avaiable_troups += value

    def decrease_avaiable_troups(self, value):
        if(value>=0):
            value = self.avaiable_troups - value
            if(value<0):
                raise Exception("Invalid number of troups")
            self.avaiable_troups = value

    # def add_country(self, country_id):
    #     ids = self.get_countries()
    #     if(not(country_id in ids)):
    #         self.owned.append((country_id, 1))
    #
    # def remove_country(self, country_id):
    #     ids = self.get_countries()
    #     if(country_id in ids):
    #         index = ids.index(country_id)
    #         self.owned.pop(index)
    #
    # def get_country_troups(self, country_id):
    #     ids = self.get_countries()
    #     if(country_id in ids):
    #         index = self.index(country_id)
    #         return self.owned[index][1] #Returning the number of troups
    #
    # def add_country_troups(self, country_id, value):
    #     ids = self.get_countries()
    #     if((value >= 0)and(country_id in ids)):
    #         index = ids.index(country_id)
    #         self.owned[index][1] += value
    #
    # def remove_country_troups(self, country_id, value):
    #     ids = self.get_countries()
    #     if((value >= 0)and(country_id in ids)):
    #         index = ids.index(country_id)
    #         value = self.owned[index][1]-value
    #         if(value<0):
    #             value = 0 #Negative values are not allowed
    #         self.owned[index][1] = value
