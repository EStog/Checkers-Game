# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import OperatorEat

class OperatorEatForDark(OperatorEat.OperatorEat):
    '''
    classdocs
    '''

    def applyOperator(self, gameboard, givePosis = False):

        self.waylength = 1; sol = []; k = 0; i = gameboard.placesCount

        offsetUpFar = gameboard.offsetUpFar
        offsetDownFar = gameboard.offsetDownFar

        while k < gameboard.halfDimension:

            offsetUp = gameboard.halfDimension - 1
            offsetDown = gameboard.halfDimension + 1
            i -= gameboard.halfDimension
            max1, sol1 = self._eat(i, offsetUp, offsetDown, offsetUpFar, offsetDownFar, 1,
                                   self._darkPieceEat, self._possibleDarkQueenEat,
                                   self._darkQueenEat, gameboard.emptyDarkPiece,
                                   gameboard.emptyDarkQueen, gameboard)
            if max1 > self.waylength:
                sol = []
                self.waylength = max1
                sol.extend(sol1)
            elif max1 != 0 and max1 == self.waylength:
                sol.extend(sol1)

            offsetUp = gameboard.halfDimension
            offsetDown = gameboard.halfDimension
            i -= gameboard.halfDimension
            max1, sol1 = self._eat(i, offsetUp, offsetDown, offsetUpFar, offsetDownFar, 1,
                                   self._darkPieceEat, self._possibleDarkQueenEat,
                                   self._darkQueenEat, gameboard.emptyDarkPiece,
                                   gameboard.emptyDarkQueen, gameboard)
            if max1 > self.waylength:
                sol = []
                self.waylength = max1
                sol.extend(sol1)
            elif max1 != 0 and max1 == self.waylength:
                sol.extend(sol1)

            k += 1

        if givePosis:
            yield sol
        else:
            yield len(sol) > 0

        for w in self._giveWays(sol, offsetDownFar, offsetUpFar, 1,
                                   self._darkPieceEat, self._possibleDarkQueenEat,
                                   self._darkQueenEat, gameboard):
            yield w
