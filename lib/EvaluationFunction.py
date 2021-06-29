# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import Singleton, OperatorMoveForDark, OperatorMoveForLight, OperatorEatForDark, OperatorEatForLight, Gameboard

INFINITY = 1000000
_UPRIGHT = 0
_UPLEFT = 1
_DOWNRIGHT = 2
_DOWNLEFT = 3

class EvaluationFunction(Singleton.Singleton):
    '''
    classdocs
    '''

    def __givej(self, i, gameboard):
        offsetUp = gameboard.halfDimension - ( (i/gameboard.halfDimension) % 2 )
        offsetDown = gameboard.halfDimension + ( (i/gameboard.halfDimension) % 2 )
        yield i + offsetUp, _UPRIGHT
        yield i + offsetUp + 1, _UPLEFT
        yield i - offsetDown, _DOWNRIGHT
        yield i - offsetDown + 1, _DOWNLEFT


    def __markAdjacents(self, i, mark, emptyP, gameboard):
        op = { _UPRIGHT: _DOWNLEFT, _UPLEFT : _DOWNRIGHT, _DOWNRIGHT: _UPLEFT, _DOWNLEFT: _UPRIGHT }
        queue = []
        queue.append(i)
        while len(queue) > 0:
            i = queue.pop(0)
            queue1 = []
            ok =  False
            direction = -1
            for j, _direction in self.__givej(i, gameboard):
                if ( gameboard.inRightRange(j) and
                     gameboard._validShift(i, j) ):
                    if not emptyP(gameboard, j):
                        if direction == -1:
                            direction = _direction
                        elif _direction != op[direction] :
                            ok = True
                        if not mark[j]:
                            queue1.append(j)
                else:
                    if direction == -1:
                        direction = _direction
                    elif _direction != op[direction] :
                        ok = True
            if ok:
                for x in queue1:
                    mark[x] = True
                queue.extend(queue1)
            else:
                mark[i] = False


    def __dispersionFactor(self, emptyP, count, gameboard):
        c = 0
        i = 0
        mark = []
        sol = 0
        for _ in xrange(0, gameboard.placesCount):
            mark.append(False)
        while c < count:
            if not emptyP(gameboard, i):
                c += 1
                if not mark[i]:
                    sol += 1
                    mark[i] = True
                    self.__markAdjacents(i, mark, emptyP, gameboard)
                    mark[i] = True
            i += 1

        return sol


    def __darkDispersionFactor(self, gameboard):
        return self.__dispersionFactor( Gameboard.Gameboard.emptyDark,
                                        gameboard.darkPiecesCount + gameboard.darkQueensCount,
                                        gameboard )


    def __lightDispersionFactor(self, gameboard):
        return self.__dispersionFactor( Gameboard.Gameboard.emptyLight,
                                        gameboard.lightPiecesCount + gameboard.lightQueensCount,
                                        gameboard )


    def evaluate(self, gameboard):

        totalDarks = float( gameboard.darkPiecesCount + gameboard.darkQueensCount )
        totalLights = gameboard.lightPiecesCount + gameboard.lightQueensCount

        darkQueensCount = float( gameboard.darkQueensCount )
        lightQueensCount = gameboard.lightQueensCount

        darkDispersionFactor = float( self.__darkDispersionFactor(gameboard) )
        lightDispersionFactor = self.__lightDispersionFactor(gameboard)

        operatorMoveForDark = OperatorMoveForDark.OperatorMoveForDark()
        operatorMoveForLight = OperatorMoveForLight.OperatorMoveForLight()
#        operatorEatForDark = OperatorEatForDark.OperatorEatForDark()
#        operatorEatForLight = OperatorEatForLight.OperatorEatForLight()

#        eatDarkPosibilitiesCount = float( operatorEatForDark.posibilitiesCount(gameboard) )
#        eatLightPosibilitiesCount = operatorEatForLight.posibilitiesCount(gameboard)
        moveDarkPosibilitiesCount = float( operatorMoveForDark.posibilitiesCount(gameboard) )
        moveLightPosibilitiesCount = operatorMoveForLight.posibilitiesCount(gameboard)
        darkPosibilitiesCount = moveDarkPosibilitiesCount
        lightPosibilitiesCount = moveLightPosibilitiesCount
#        darkPosibilitiesCount = eatDarkPosibilitiesCount
#        lightPosibilitiesCount = eatLightPosibilitiesCount


#        if eatDarkPosibilitiesCount == 0:
#            darkPosibilitiesCount = moveDarkPosibilitiesCount
#
#        if eatLightPosibilitiesCount == 0:
#            lightPosibilitiesCount = moveLightPosibilitiesCount
#
#        elif eatDarkPosibilitiesCount > 0 and eatLightPosibilitiesCount > 0:
#            darkPosibilitiesCount += moveDarkPosibilitiesCount
#            lightPosibilitiesCount += moveLightPosibilitiesCount

        if totalDarks == 0 or darkPosibilitiesCount == 0:
            return INFINITY

        if totalLights == 0 or lightPosibilitiesCount == 0:
            return -INFINITY

        return (
                    4 * (
                            (totalLights+1) / (totalDarks+1) +
                            totalLights - totalDarks
                        ) +

                    3 * (
                            (lightQueensCount+1) / (darkQueensCount+1) +
                            lightQueensCount - darkQueensCount
                        ) +

                    2 * (
                            (darkDispersionFactor+1) / (lightDispersionFactor+1) +
                            darkDispersionFactor - lightDispersionFactor
                        ) +

                        (
                            (lightPosibilitiesCount+1) / (darkPosibilitiesCount+1) +
                            lightPosibilitiesCount - darkPosibilitiesCount
                        )
               )
