# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import Singleton

class Operator(Singleton.Singleton):
    '''
    classdocs
    '''

    def _validShift(self, i, destination, gameboard):
        return gameboard._validShift(i, destination)

    def applyOperator(self, gameboard):
        raise "abstract method"

    def posibilitiesCount(self, gameboard):
        count = 0

        for _ in self.applyOperator(gameboard):
            count += 1

        return count
