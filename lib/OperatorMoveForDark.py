# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import OperatorMove, Gameboard

class OperatorMoveForDark(OperatorMove.OperatorMove):
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
        i = gameboard.placesCount

        while k < gameboard.halfDimension:

            offsetUp = gameboard.halfDimension - 1
            offsetDown = gameboard.halfDimension + 1
            i -= gameboard.halfDimension
            for x in self._move(i, offsetUp, offsetDown, 1, self._moveDarkPiece,
                                Gameboard.Gameboard.moveDirectlyDarkQueen,
                                gameboard.emptyDarkPiece, gameboard.emptyDarkQueen, gameboard):
                yield x

            offsetUp = gameboard.halfDimension
            offsetDown = gameboard.halfDimension
            i -= gameboard.halfDimension
            for x in self._move(i, offsetUp, offsetDown, 1, self._moveDarkPiece,
                                Gameboard.Gameboard.moveDirectlyDarkQueen,
                                gameboard.emptyDarkPiece, gameboard.emptyDarkQueen, gameboard):
                yield x

            k += 1
