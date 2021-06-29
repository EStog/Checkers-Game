# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import Operator, AnEatMove, Gameboard

_UPRIGHT = 0
_UPLEFT = 1
_DOWNRIGHT = 2
_DOWNLEFT = 3


class OperatorEat(Operator.Operator):
    '''
    classdocs
    '''

    def __init__(self):
        Operator.Operator.__init__(self)
        self.waylength = None


    def __applyPieceEat(self, x, pieceEat, gameboard):
        board = gameboard.clone()
        offsetUpFar = board.offsetUpFar
        offsetDownFar = board.offsetDownFar
        i = x[0]
        offsetUp = board.halfDimension - ( (i/board.halfDimension) % 2 )
        offsetDown = board.halfDimension + ( (i/board.halfDimension) % 2 )
        k = 1
        xLenght = len(x)
        direction = -1
        while k < xLenght:
            j = x[k]
            ok = False
            for b, j1, _direction in self.__possiblePieceEat(i, direction, offsetUp, offsetDown, offsetUpFar, offsetDownFar):
                if j == j1:
                    direction = _direction; ok = True; break
            if ok:
                board = pieceEat(i, b, j, board)
            else:
                return None
            if not board:
                return None
            i = j
            k += 1

        return board


    def __applyQueenEat(self, x, queenEat, emptyOpposite, gameboard):
        board = gameboard.clone()
        i = x[0]
        offsetUp = board.halfDimension - ( (i/board.halfDimension) % 2 )
        offsetDown = board.halfDimension + ( (i/board.halfDimension) % 2 )
        k = 1
        xLenght = len(x)
        direction = -1
        while k < xLenght:
            j = x[k]
            ok = False
            for b, j1, _direction in self.__possibleQueenEat(i, direction, offsetUp, offsetDown, emptyOpposite, board):
                if j == j1:
                    direction = _direction; ok = True; break
            if ok:
                board = queenEat(i, b, j, board)
            else:
                return None
            if not board:
                return None
            i = j
            offsetUp = board.halfDimension - ( (i/board.halfDimension) % 2 )
            offsetDown = board.halfDimension + ( (i/board.halfDimension) % 2 )
            k += 1

        return board


    def applyEat(self, x, playDark, gameboard):
        if playDark:
            if not gameboard.emptyDarkPiece(x[0]):
                return self.__applyPieceEat(x, self._darkPieceEat, gameboard)
            else:
                return self.__applyQueenEat(x, self._darkQueenEat, Gameboard.Gameboard.emptyLight, gameboard)
        else:
            if not gameboard.emptyLightPiece(x[0]):
                return self.__applyPieceEat(x, self._lightPieceEat, gameboard)
            else:
                return self.__applyQueenEat(x, self._lightQueenEat, Gameboard.Gameboard.emptyDark, gameboard)


    def _darkPieceEat(self, i, between, destination, gameboard):
        board = None
        if not gameboard.inRightRange(between):
            return None
        if self._validShift(i, between, gameboard) and self._validShift(between, destination, gameboard):
            if not gameboard.emptyLightPiece(between):
                board = gameboard.moveDirectlyDarkPiece(i, destination)
                if board:
                    board.lightPieces ^= 1 << between
                    board.lightPiecesCount -= 1
            elif not gameboard.emptyLightQueen(between):
                board = gameboard.moveDirectlyDarkPiece(i, destination)
                if board:
                    board.lightQueens ^= 1 << between
                    board.lightQueensCount -= 1

        return board


    def _lightPieceEat(self, i, between, destination, gameboard):
        board = None
        if not gameboard.inRightRange(between):
            return None
        if self._validShift(i, between, gameboard) and self._validShift(between, destination, gameboard):
            if not gameboard.emptyDarkPiece(between):
                board = gameboard.moveDirectlyLightPiece(i, destination)
                if board:
                    board.darkPieces ^= 1 << between
                    board.darkPiecesCount -= 1
            elif not gameboard.emptyDarkQueen(between):
                board = gameboard.moveDirectlyLightPiece(i, destination)
                if board:
                    board.darkQueens ^= 1 << between
                    board.darkQueensCount -= 1

        return board


    def _darkQueenEat(self, i, between, destination, gameboard):
        board = gameboard.clone()
        board.darkQueens = gameboard.darkQueens ^ ( (1 << i) + (1 << destination) )
        if not gameboard.emptyLightPiece(between):
            board.lightPieces ^= 1 << between
            board.lightPiecesCount -= 1
        elif not gameboard.emptyLightQueen(between):
            board.lightQueens ^= 1 << between
            board.lightQueensCount -= 1

        return board


    def _lightQueenEat(self, i, between, destination, gameboard):
        board = gameboard.clone()
        board.lightQueens = gameboard.lightQueens ^ ( (1 << i) + (1 << destination) )
        if not gameboard.emptyDarkPiece(between):
            board.darkPieces ^= 1 << between
            board.darkPiecesCount -= 1
        elif not gameboard.emptyDarkQueen(between) :
            board.darkQueens ^= 1 << between
            board.darkQueensCount -= 1

        return board


    def __possiblePieceEat(self, i, ndirection, offsetUp, offsetDown, offsetUpFar, offsetDownFar):
        if ndirection != _UPRIGHT:
            yield i + offsetUp, i + offsetUpFar, _DOWNLEFT
        if ndirection != _UPLEFT:
            yield i + offsetUp + 1, i + offsetUpFar + 2, _DOWNRIGHT
        if ndirection != _DOWNRIGHT:
            yield i - offsetDown, i - offsetDownFar, _UPLEFT
        if ndirection != _DOWNLEFT:
            yield i - offsetDown + 1, i - offsetDownFar + 2, _UPRIGHT


    def __pieceEatLength(self, i, offsetUp, offsetDown, offsetUpFar, offsetDownFar, pieceEat, gameboard):
        length = 0
        queue = [(i, -1, gameboard, 0)]
        while len(queue) > 0:
            i, direction, board, cost = queue.pop(0)
            if cost > length:
                length = cost
            for i1, i2, _direction in self.__possiblePieceEat(i, direction, offsetUp, offsetDown, offsetUpFar, offsetDownFar):
                newBoard = pieceEat(i, i1, i2, board)
                if newBoard:
                    queue.append( (i2, _direction, newBoard, cost+1) )
        return length


    def __pieceEat(self, i, offsetUp, offsetDown, offsetUpFar, offsetDownFar, pieceEat, gameboard):

        way = []; ways = []

        def __pieceEatSearch(i, direction, gameboard):
            if len(way) == self.waylength:
                way1 = []; ok = True
                for _, board in ways:
                    if board == gameboard:
                        ok = False; break
                if ok:
                    for w in way:
                        way1.append(w)
                    ways.append( (way1, gameboard) )
            else:
                for i1, i2, _direction in self.__possiblePieceEat(i, direction, offsetUp, offsetDown, offsetUpFar, offsetDownFar):
                    newBoard = pieceEat(i, i1, i2, gameboard)
                    if newBoard:
                        way.append( AnEatMove.AnEatMove(i, i1, i2) )
                        __pieceEatSearch( i2, _direction, newBoard )
                        way.pop()

        __pieceEatSearch(i, -1, gameboard)
        for w in ways:
            yield w


    def __possibleQueenEatInOneDirection(self, i, offset, dif, emptyOpposite, gameboard):
        j = i
        destination = j + offset
        while ( gameboard.inRightRange(destination) and
                self._validShift(j, destination, gameboard) and
                gameboard.empty(destination) ):
            j = destination
            if abs(offset) == gameboard.halfDimension:
                offset += dif
            else:
                offset -= dif
            destination = j + offset

        if ( not gameboard.inRightRange(destination) or
             not self._validShift(j, destination, gameboard) or
             emptyOpposite(gameboard, destination) ):
            return

        between = destination

        j = destination
        if abs(offset) == gameboard.halfDimension:
                offset += dif
        else:
            offset -= dif
        destination = j + offset
        while ( gameboard.inRightRange(destination) and
                self._validShift(j, destination, gameboard) and
                gameboard.empty(destination) ):
            yield between, destination
            j = destination
            if abs(offset) == gameboard.halfDimension:
                offset += dif
            else:
                offset -= dif
            destination = j + offset


    def __possibleQueenEat(self, i, ndirection, offsetUp, offsetDown, emptyOpposite, gameboard):
        if ndirection != _UPRIGHT:
            for i1, i2 in self.__possibleQueenEatInOneDirection(i, offsetUp, -1, emptyOpposite, gameboard):
                yield i1, i2, _DOWNLEFT
        if ndirection != _UPLEFT:
            for i1, i2 in self.__possibleQueenEatInOneDirection(i, offsetUp + 1, 1, emptyOpposite, gameboard):
                yield i1, i2, _DOWNRIGHT
        if ndirection != _DOWNRIGHT:
            for i1, i2 in self.__possibleQueenEatInOneDirection(i, -offsetDown, -1, emptyOpposite, gameboard):
                yield i1, i2, _UPLEFT
        if ndirection != _DOWNLEFT:
            for i1, i2 in self.__possibleQueenEatInOneDirection(i, -offsetDown + 1, 1, emptyOpposite, gameboard):
                yield i1, i2, _UPRIGHT


    def _possibleLightQueenEat(self, i, ndirection, offsetUp, offsetDown, gameboard):
        return self.__possibleQueenEat(i, ndirection, offsetUp, offsetDown, Gameboard.Gameboard.emptyDark, gameboard)


    def _possibleDarkQueenEat(self, i, ndirection, offsetUp, offsetDown, gameboard):
        return self.__possibleQueenEat(i, ndirection, offsetUp, offsetDown, Gameboard.Gameboard.emptyLight, gameboard)


    def __queenEatLength(self, i, posibleQueenEat, queenEat, gameboard):
        length = 0
        queue = [(i, -1, gameboard, 0)]
        while len(queue) > 0:
            i, direction, gameboard, cost = queue.pop(0)
            x = (i / gameboard.halfDimension) % 2
            offsetUp = gameboard.halfDimension - x
            offsetDown = gameboard.halfDimension + x
            if cost > length:
                length = cost
            for i1, i2, _direction in posibleQueenEat(i, direction, offsetUp, offsetDown, gameboard):
                newBoard = queenEat(i, i1, i2, gameboard)
                queue.append( (i2, _direction, newBoard, cost+1) )

        return length


    def __queenEat(self, i, posibleQueenEat, queenEat, gameboard):

        way = []; ways = []

        def __queenEatSearch(i, direction, gameboard):
            if len(way) == self.waylength:
                way1 = []; ok = True
                for _, board in ways:
                    if board == gameboard:
                        ok = False; break
                if ok:
                    for w in way:
                        way1.append(w)
                    ways.append( (way1, gameboard) )
            else:
                x = (i / gameboard.halfDimension) % 2
                offsetUp = gameboard.halfDimension - x
                offsetDown = gameboard.halfDimension + x
                for i1, i2, _direction in posibleQueenEat(i, direction, offsetUp, offsetDown, gameboard):
                    newBoard = queenEat(i, i1, i2, gameboard)
                    way.append( AnEatMove.AnEatMove(i, i1, i2) )
                    __queenEatSearch( i2, _direction, newBoard)
                    way.pop()

        __queenEatSearch(i, -1, gameboard)
        for w in ways:
            yield w


    def _eat(self, i, offsetUp, offsetDown, offsetUpFar, offsetDownFar, sign, pieceEat,
             posibleQueenEat, queenEat, emptyPiece, emptyQueen, gameboard):

        maxi = 0; sol = []
        j = i + gameboard.halfDimension
        while i < j:
            l1 = 0; l2 = 0
            if not emptyPiece(i):
                l1 = self.__pieceEatLength(i, offsetUp, offsetDown, offsetUpFar, offsetDownFar, pieceEat, gameboard)
            if not emptyQueen(i):
                l2 = self.__queenEatLength(i, posibleQueenEat, queenEat, gameboard)

            if l1 > l2:
                l = l1; wasPiece = True
            else:
                l = l2; wasPiece = False

            if maxi < l:
                maxi = l; sol = []; sol.append( (i, offsetUp, offsetDown, wasPiece) )
            elif l != 0 and maxi == l:
                sol.append( (i, offsetUp, offsetDown, wasPiece) )
            i += 1

        return maxi, sol


    def _giveWays(self, sol, offsetDownFar, offsetUpFar, sign, pieceEat, posibleQueenEat, queenEat, gameboard):
        for s in sol:
            pos, offsetUp, offsetDown, wasPiece = s
            if self.waylength > 0:
                if wasPiece:
                    for w in self.__pieceEat(pos, offsetUp, offsetDown, offsetUpFar, offsetDownFar, pieceEat, gameboard):
                        yield w

                else:
                    for w in self.__queenEat(pos, posibleQueenEat, queenEat, gameboard):
                        yield w


    def posibilitiesCount(self, gameboard):
        count = 0

        ways = self.applyOperator(gameboard)
        if ways.next():
            for _ in ways:
                count += 1

        return count
