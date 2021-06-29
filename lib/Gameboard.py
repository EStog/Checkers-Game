# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''


class Gameboard(object):
    '''
    classdocs
    '''

    def __init__(self, dimension = 8, piecesCount = 12):
        '''
        Constructor
        '''
        self.canApplyBlow = False
        self.darkQueens = 0
        self.darkQueensCount = 0
        self.lightQueens = 0
        self.lightQueensCount = 0
        self.__setVariables(dimension, piecesCount)
        self.__initializePieces()


    def __str__(self):
        return "Gameboard:\n" + \
               "    Dark pieces:  " + str(self.darkPieces) + "\n" + \
               "    Dark pieces amount: " + str(self.darkPiecesCount) + "\n" + \
               "    Dark queens:  " + str(self.darkQueens) + "\n" + \
               "    Dark queens amount: " + str(self.darkQueensCount) + "\n" + \
               "    Light pieces: " + str(self.lightPieces) + "\n" + \
               "    Light pieces amount: " + str(self.lightPiecesCount) + "\n" + \
               "    Light queens: " + str(self.lightQueens) + "\n" + \
               "    Light queens amount: " + str(self.lightQueensCount) + "\n"


    def __eq__(self, board):
        return self.darkPieces == board.darkPieces and self.darkQueens == board.darkQueens and \
               self.lightPieces == board.lightPieces and self.lightQueens == board.lightQueens


    def __setVariables(self, dimension = 8, piecesCount = 12):
        self.dimension = dimension
        self.placesCount = (self.dimension * self.dimension) / 2
        self.halfDimension = self.dimension / 2
        self.__beginOfFirstLine = 0
        self.__endOfFirstLine = self.__beginOfFirstLine + self.halfDimension - 1
        self.__beginOfLastLine = self.placesCount - self.halfDimension
        self.__endOfLastLine = self.__beginOfLastLine + self.halfDimension - 1
        self.initialPiecesCount = piecesCount
        self.offsetUpFar = self.halfDimension + self.halfDimension - 1
        self.offsetDownFar = self.halfDimension + self.halfDimension + 1


    def __initializePieces(self):
        self.darkPiecesCount = self.initialPiecesCount
        self.lightPiecesCount = self.initialPiecesCount
        self.darkPieces = (1 << self.initialPiecesCount) - 1
        self.lightPieces = self.darkPieces * ( 1 << (self.placesCount - self.initialPiecesCount) )


    def clone(self):
        gameboard = Gameboard(self.dimension, self.initialPiecesCount)
        gameboard.darkPieces = self.darkPieces
        gameboard.darkPiecesCount = self.darkPiecesCount

        gameboard.lightPieces = self.lightPieces
        gameboard.lightPiecesCount = self.lightPiecesCount

        gameboard.darkQueens = self.darkQueens
        gameboard.darkQueensCount = self.darkQueensCount

        gameboard.lightQueens = self.lightQueens
        gameboard.lightQueensCount = self.lightQueensCount

        return gameboard


    def empty(self, i):
        temp = 1 << i
        return (self.darkPieces & temp) == 0 and \
               (self.lightPieces & temp) == 0 and \
               (self.darkQueens & temp) == 0 and \
               (self.lightQueens & temp) == 0


    def emptyDark(self, i):
        return self.emptyDarkPiece(i) and self.emptyDarkQueen(i)


    def emptyLight(self, i):
        return self.emptyLightPiece(i) and self.emptyLightQueen(i)


    def emptyDarkPiece(self, i):
        return (self.darkPieces & (1 << i)) == 0


    def emptyDarkQueen(self, i):
        return (self.darkQueens & (1 << i)) == 0


    def emptyLightPiece(self, i):
        return (self.lightPieces & (1 << i)) == 0


    def emptyLightQueen(self, i):
        return (self.lightQueens & (1 << i)) == 0


    def inRightRange(self, destination):
        return destination > -1 and destination < self.placesCount


    def moveDirectlyDarkPiece(self, i, destination):

        if not self.inRightRange(destination):
            return None

        #if not self.emptyDarkPiece(i) and self.empty(destination):
        if self.empty(destination):
            board = self.clone()
            if destination >= self.__beginOfLastLine and destination <= self.__endOfLastLine:
                board.darkPieces ^= 1 << i
                board.darkPiecesCount -= 1
                board.darkQueens ^= 1 << destination
                board.darkQueensCount += 1
            else:
                board.darkPieces = self.darkPieces ^ ( (1 << i) + (1 << destination) )
            return board

        return None


    def moveDirectlyDarkQueen(self, i, destination):

        if not self.inRightRange(destination):
            return None

        #if not self.emptyDarkQueen(i) and self.empty(destination):
        if self.empty(destination):
            board = self.clone()
            board.darkQueens = self.darkQueens ^ ( (1 << i) + (1 << destination) )
            return board

        return None


    def moveDirectlyLightPiece(self, i, destination):

        if not self.inRightRange(destination):
            return None

        #if not self.emptyLightPiece(i) and self.empty(destination):
        if self.empty(destination):
            board = self.clone()
            if destination >= self.__beginOfFirstLine and destination <= self.__endOfFirstLine:
                board.lightPieces ^= 1 << i
                board.lightPiecesCount -= 1
                board.lightQueens ^= 1 << destination
                board.lightQueensCount += 1
            else:
                board.lightPieces = self.lightPieces ^ ( (1 << i) + (1 << destination) )
            return board

        return None


    def moveDirectlyLightQueen(self, i, destination):

        if not self.inRightRange(destination):
            return None

        #if not self.emptyLightQueen(i) and self.empty(destination):
        if self.empty(destination):
            board = self.clone()
            board.lightQueens = self.lightQueens ^ ( (1 << i) + (1 << destination) )
            return board

        return None

    def _validShift(self, i, destination):
        return (
                    ( (i - self.halfDimension) % self.dimension != 0 or
                        (
                            destination != i + self.halfDimension - 1 and
                            destination != i - self.halfDimension - 1
                        )
                    ) and
                    ( (i - self.halfDimension + 1) % self.dimension != 0 or
                        (
                            destination != i + self.halfDimension + 1 and
                            destination != i - self.halfDimension + 1
                        )
                    )
               )
