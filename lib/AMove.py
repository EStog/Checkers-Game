# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

class AMove(object):
    '''
    classdocs
    '''


    def __init__(self, ini, destination):
        '''
        Constructor
        '''
        self.ini = ini
        self.destination = destination

    def __str__(self):
        return "Move:\n" + \
               "    source: " + str(self.ini) + "\n" +\
               "    destination: " + str(self.destination) + "\n"
