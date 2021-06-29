# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import OperatorMove, Gameboard

class OperatorMoveForLight(OperatorMove.OperatorMove):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        OperatorMove.OperatorMove.__init__(self)


    def applyOperator(self, gameboard):

        k = 0
        i = -gameboard.halfDimension
        while k < gameboard.halfDimension:

            offsetUp = gameboard.halfDimension
            offsetDown = gameboard.halfDimension
            i += gameboard.halfDimension
            for x in self._move(i, offsetUp, offsetDown, -1, self._moveLightPiece,
                                Gameboard.Gameboard.moveDirectlyLightQueen,
                                gameboard.emptyLightPiece, gameboard.emptyLightQueen, gameboard):
                yield x

            offsetDown += 1
            offsetUp -= 1
            i += gameboard.halfDimension
            for x in self._move(i, offsetUp, offsetDown, -1, self._moveLightPiece,
                                Gameboard.Gameboard.moveDirectlyLightQueen,
                                gameboard.emptyLightPiece, gameboard.emptyLightQueen, gameboard):
                yield x

            k += 1
