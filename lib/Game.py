# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import OperatorEatForLight, OperatorEatForDark, OperatorMoveForDark, OperatorMoveForLight, Gameboard, EvaluationFunction
from EvaluationFunction import INFINITY

class Game(object):
    '''
    classdocs
    '''

    def __init__( self, dimension = 8, piecesCount = 12,
                  userPlayDarks = True, maxDepth = 5,
                  operatorEatForDark = OperatorEatForDark.OperatorEatForDark(),
                  operatorEatForLight = OperatorEatForLight.OperatorEatForLight(),
                  operatorMoveForDark = OperatorMoveForDark.OperatorMoveForDark(),
                  operatorMoveForLight = OperatorMoveForLight.OperatorMoveForLight(),
                  evaluationFunction = EvaluationFunction.EvaluationFunction() ):
        '''
        Constructor
        '''
        self.gameboard = Gameboard.Gameboard(dimension, piecesCount)
        self.operatorEatForDark = operatorEatForDark
        self.operatorEatForLight = operatorEatForLight
        self.operatorMoveForDark = operatorMoveForDark
        self.operatorMoveForLight = operatorMoveForLight
        self.__evaluationFunction = evaluationFunction
        self.__maxDepth = maxDepth
        self.__initialDepth = maxDepth
        self.__maxDepthFound = 0
        self.userPlayDarks = userPlayDarks


    def canPlay(self, playerDark):
        if playerDark == True:
            return self.__canPlay( self.operatorMoveForDark, self.operatorEatForDark,
                                   self.gameboard.darkPiecesCount + self.gameboard.darkQueensCount )
        else:
            return self.__canPlay( self.operatorMoveForLight, self.operatorEatForLight,
                                   self.gameboard.lightPiecesCount + self.gameboard.lightQueensCount )


    def __canPlay(self, operatorMove, operatorEat, count):
        return (
                    count > 0 and
                    (
                        operatorEat.posibilitiesCount(self.gameboard) > 0 or
                        operatorMove.posibilitiesCount(self.gameboard) > 0
                    )
               )


    def __compareForDark(self, alfa, beta, alfa1, beta1):
        if alfa1 < beta:
            beta = alfa1
        return alfa, beta


    def __compareForLight(self, alfa, beta, alfa1, beta1):
        if beta1 > alfa:
            alfa = beta1
        return alfa, beta


    def __compareForDark1(self, alfa, beta, alfa1, beta1, sol, sol1, board, board1):
        if alfa1 < beta:
            beta = alfa1
            sol = sol1
            board = board1
        return alfa, beta, sol, board


    def __compareForLight1(self, alfa, beta, alfa1, beta1, sol, sol1, board, board1):
        if beta1 > alfa:
            alfa = beta1
            sol = sol1
            board = board1
        return alfa, beta, sol, board


    def __rAlfaBetaForDark(self, value):
        return None, value


    def __rAlfaBetaForLight(self, value):
        return value, None


    def FindNextMove(self):

        operatorsEat = { True: self.operatorEatForDark, False: self.operatorEatForLight }
        operatorsMove = { True: self.operatorMoveForDark, False: self.operatorMoveForLight }
        comparators = { True: self.__compareForDark, False: self.__compareForLight }
        rAlfaBeta = { True: self.__rAlfaBetaForDark, False: self.__rAlfaBetaForLight }
        comparators1 = { True: self.__compareForDark1, False: self.__compareForLight1 }

        def __FindNextMove(depth, gameboard, alfa, beta, playDarks):
            mustEat = True
            if operatorsEat[not playDarks].applyOperator(gameboard).next():
                mustEat = False
            ways = operatorsEat[playDarks].applyOperator(gameboard)
            if ways.next():
                for _, board in ways:
                    alfa1, beta1 = __FindNextMove(depth + 1, board, alfa, beta, not playDarks)
                    alfa, beta = comparators[playDarks](alfa, beta, alfa1, beta1)
                    if alfa >= beta:
                        mustEat = True
                        self.__cutCount += 1
                        break
            else:
                mustEat = False
            if not mustEat:
                if depth >= self.__maxDepth:
                    if depth > self.__maxDepthFound:
                        self.__maxDepthFound = depth
                    self.__scannedWays += 1
                    value = self.__evaluationFunction.evaluate(gameboard)
                    alfa, beta = rAlfaBeta[playDarks](value)
                else:
                    board = None
                    for _, board in operatorsMove[playDarks].applyOperator(gameboard):
                        alfa1, beta1 = __FindNextMove(depth + 1, board, alfa, beta, not playDarks)
                        alfa, beta = comparators[playDarks](alfa, beta, alfa1, beta1)
                        if alfa >= beta:
                            self.__cutCount += 1
                            break
                    else:
                        if not board:
                            if depth > self.__maxDepthFound:
                                self.__maxDepthFound = depth
                            self.__scannedWays += 1
                            value = self.__evaluationFunction.evaluate(gameboard)
                            alfa, beta = rAlfaBeta[playDarks](value)

            return alfa, beta


        if self.gameboard.darkQueensCount + self.gameboard.lightQueensCount > 0:
            self.__maxDepth = self.__initialDepth
        else:
            #Para lograr que la profundidad aumente la misma proporción de lo que ha disminuido la cantida de piezas.
            #o sea, si la cantidad de piezas disminuye en un 30% que la profundidad máxima aumente en su propio 30%
            #(o en una fracción de ella para que la profundidad no aumente demasiado rápido).
            dc = ( self.gameboard.initialPiecesCount*2 - self.gameboard.darkPiecesCount -
                   self.gameboard.darkQueensCount - self.gameboard.lightPiecesCount -
                   self.gameboard.lightQueensCount ) #dc es la cantidad que ha disminuido la cantidad de piezas.
            sConst = self.__initialDepth - 1#0.5
            # sConst es para lograr que no aumente demasiado rápido.
            # Esta constante nunca debe ser mayor que la profundidad inicial,
            # si no la profundidad nunca aumentará.
            self.__maxDepth = self.__initialDepth + int( (dc * self.__initialDepth) / (self.gameboard.initialPiecesCount*2 * sConst) )


        self.__maxDepthFound = 0
        self.__cutCount = 0
        self.__scannedWays = 0

        print ""
        print "Depth upper bound: " + str(self.__maxDepth)

        gameboard = self.gameboard.clone()

        alfa = -INFINITY; beta = INFINITY
        sol = None; sol1 = None
        mustEat = True
        if operatorsEat[self.userPlayDarks].applyOperator(self.gameboard).next():
            mustEat = False
        ways = operatorsEat[not self.userPlayDarks].applyOperator(self.gameboard)
        if ways.next():
            for sol1, board in ways:
                alfa1, beta1 = __FindNextMove(1, board, alfa, beta, self.userPlayDarks)
                alfa, beta, sol, gameboard = comparators1[not self.userPlayDarks](alfa, beta, alfa1, beta1, sol, sol1, gameboard, board)
        else:
            mustEat = False
        if not mustEat:
            for sol1, board in operatorsMove[not self.userPlayDarks].applyOperator(self.gameboard):
                alfa1, beta1 = __FindNextMove(1, board, alfa, beta, self.userPlayDarks)
                alfa, beta, sol, gameboard = comparators1[not self.userPlayDarks](alfa, beta, alfa1, beta1, sol, sol1, gameboard, board)

        self.gameboard = gameboard

        print "Maximum depth reached: " + str(self.__maxDepthFound)
        print "Scanned ways: " + str(self.__scannedWays)
        print "Cuts: " + str(self.__cutCount)
        print "Alfa: " + str(alfa)
        print "Beta: " + str(beta)
        print "Gameboard evaluation: " + str(self.__evaluationFunction.evaluate(self.gameboard))
        print self.gameboard
        if sol == None:
            sol = sol1

        return sol


#game = Game(maxDepth=4)
#print game.FindNextMove(True)
#print game.gameboard

#import Gameboard, OperatorEatForDark, OperatorEatForLight
#import OperatorMoveForDark, OperatorMoveForLight, EvaluationFunction
#
#b = Gameboard.Gameboard()
#oe = OperatorEatForDark.OperatorEatForDark()
#oe1 = OperatorEatForLight.OperatorEatForLight()
#o = OperatorMoveForDark.OperatorMoveForDark()
#o1 = OperatorMoveForLight.OperatorMoveForLight()
#
#b.darkQueens = 1048576
#b.darkPieces = 0
#b.lightPieces = 69215232
#b.lightQueens = 0
#
#f = EvaluationFunction.EvaluationFunction()
#
#print "\n"
#print f.evaluate(b)
#
#print "\n"
#for x in oe.applyOperator(b):
#    print x
#    print x[0]
#    print x[1]
#    print "\n"
