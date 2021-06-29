# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

class AnEatMove(object):
    '''
    classdocs
    '''

    def __init__(self, ini, between, destination):
        '''
        Constructor
        '''
        self.ini = ini
        self.between = between
        self.destination = destination

    def alike(self, ini, destination):
        return self.ini == ini and self.destination == destination

    def __str__(self):
        return "Eat move:\n" + \
               "    source: " + str(self.ini) +  "\n" + \
               "    between: "+ str(self.between) + "\n" + \
               "    destination: " + str(self.destination) + "\n"
