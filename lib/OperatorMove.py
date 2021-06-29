# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import Operator, AMove, Gameboard

class OperatorMove(Operator.Operator):
    '''
    classdocs
    '''

    def validMoveDarkPiece(self, i, destination, gameboard):
        if gameboard.emptyDarkPiece(i):
            return False

        offset = gameboard.halfDimension - ( (i / gameboard.halfDimension) % 2 )

        return (
                    i < destination and self._validShift(i, destination, gameboard) and
                    ( destination == i + offset or destination == i + offset + 1)
               )

    def validMoveLightPiece(self, i, destination, gameboard):
        if gameboard.emptyLightPiece(i):
            return False

        offset = gameboard.halfDimension + ( (i / gameboard.halfDimension) % 2 )

        return (
                    i > destination and self._validShift(i, destination, gameboard) and
                    ( destination == i - offset or destination == i - offset + 1)
               )


    def validMoveQueen(self, i, destination, moveQueen, gameboard):
        if i < destination:
            offset = gameboard.halfDimension - ( (i / gameboard.halfDimension) % 2 )
            for x, _ in self.__moveQueenInOneDirection(i, offset, -1, moveQueen, gameboard):
                if x.destination == destination:
                    return True
            for x, _ in self.__moveQueenInOneDirection(i, offset + 1, 1, moveQueen, gameboard):
                if x.destination == destination:
                    return True
        elif i > destination:
            offset = gameboard.halfDimension + ( (i / gameboard.halfDimension) % 2 )
            for x, _ in self.__moveQueenInOneDirection(i, -offset, -1, moveQueen, gameboard):
                if x.destination == destination:
                    return True
            for x, _ in self.__moveQueenInOneDirection(i, -offset + 1, 1, moveQueen, gameboard):
                if x.destination == destination:
                    return True

        return False


    def _moveDarkPiece(self, i, destination, gameboard):
        board = None
        if self._validShift(i, destination, gameboard):
            board = gameboard.moveDirectlyDarkPiece(i, destination)

        return board

    def _moveDarkPieceUser(self, i, destination, gameboard):
        board = None
        if self.validMoveDarkPiece(i, destination, gameboard):
            board = gameboard.moveDirectlyDarkPiece(i, destination)

        return board


    def _moveLightPiece(self, i, destination, gameboard):
        board = None
        if self._validShift(i, destination, gameboard):
            board = gameboard.moveDirectlyLightPiece(i, destination)

        return board


    def _moveLightPieceUser(self, i, destination, gameboard):
        board = None
        if self.validMoveLightPiece(i, destination, gameboard):
            board = gameboard.moveDirectlyLightPiece(i, destination)

        return board


    def _moveDarkQueenUser(self, i, destination, gameboard):
        board = None
        if ( not gameboard.emptyDarkQueen(i) and
             self.validMoveQueen(i, destination, Gameboard.Gameboard.moveDirectlyDarkQueen, gameboard) ):
            board = gameboard.moveDirectlyDarkQueen(i, destination)

        return board


    def _moveLightQueenUser(self, i, destination, gameboard):
        board = None
        if ( not gameboard.emptyLightQueen(i) and
             self.validMoveQueen(i, destination, Gameboard.Gameboard.moveDirectlyLightQueen , gameboard) ):
            board = gameboard.moveDirectlyLightQueen(i, destination)

        return board

    def __movePiece(self, i, offset, movePiece, gameboard):
        destination = i + offset
        board = movePiece(i, destination, gameboard)
        if board:
            yield AMove.AMove(i, destination), board

        destination += 1
        board = movePiece(i, destination, gameboard)
        if board:
            yield AMove.AMove(i, destination), board


    def __moveQueenInOneDirection(self, i, offset, dif, moveQueen, gameboard):
        j = i
        destination = j + offset
        if not self._validShift(j, destination, gameboard):
            return
        board = moveQueen(gameboard, i, destination)
        while board:
            yield AMove.AMove(i, destination), board
            j = destination
            if abs(offset) == gameboard.halfDimension:
                offset += dif
            else:
                offset -= dif
            destination = j + offset
            if not self._validShift(j, destination, gameboard):
                return
            board = moveQueen(gameboard, i, destination)


    def __moveQueen(self, i, offsetUp, offsetDown, moveQueen, gameboard):
        for x in self.__moveQueenInOneDirection(i, offsetUp, -1, moveQueen, gameboard):
            yield x
        for x in self.__moveQueenInOneDirection(i, offsetUp + 1, 1, moveQueen, gameboard):
            yield x
        for x in self.__moveQueenInOneDirection(i, -offsetDown, -1, moveQueen, gameboard):
            yield x
        for x in self.__moveQueenInOneDirection(i, -offsetDown + 1, 1, moveQueen, gameboard):
            yield x


    def _move(self, i, offsetUp, offsetDown, sign, movePiece, moveQueen, emptyPiece, emptyQueen, gameboard):
        offset = 0

        if sign == -1:
            offset = sign*offsetDown
        else:
            offset = sign*offsetUp

        j = i + gameboard.halfDimension
        while i < j:
            if not emptyPiece(i):
                for x in self.__movePiece(i, offset, movePiece, gameboard):
                    yield x
            elif not emptyQueen(i):
                for x in self.__moveQueen(i, offsetUp, offsetDown, moveQueen, gameboard):
                    yield x
            i += 1
