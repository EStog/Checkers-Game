# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

class Singleton(object):
    '''
    classdocs
    '''

    __instance = None

    def __new__(cls, *args, **kwargs):
        '''
        Constructor
        '''
        if cls.__instance == None:
            cls.__instance = object.__new__(cls, *args, **kwargs)
        return cls.__instance
