# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import Tkinter, Singleton, AMove, tkMessageBox, time

class GraphicalBoard(Singleton.Singleton):
    '''
    classdocs
    '''

    def __init__(self):
        self.__images = []
        self.__buttons = []
        self.__ini = None
        self.__eatMoves = []
        self.game = None
        self.parent = None


    def __refreshMove(self, x):
        t = self.__images[x.ini]['file']
        self.__images[x.ini]['file'] = "lib/images/empty.gif"
        self.__buttons[x.ini].update_idletasks()

        if not self.game.gameboard.emptyDarkQueen(x.destination):
                self.__images[x.destination]['file'] = "lib/images/darkqueen.gif"
        elif not self.game.gameboard.emptyLightQueen(x.destination):
                self.__images[x.destination]['file'] = "lib/images/lightqueen.gif"
        else:
            self.__images[x.destination]['file'] = t

        self.__buttons[x.destination].update_idletasks()


    def __refreshMoveWithAnimation(self, x):

        self.__buttons[x.ini]['relief'] = Tkinter.SUNKEN
        self.__buttons[x.ini].update_idletasks()
        time.sleep(1)
        self.__buttons[x.destination]['relief'] = Tkinter.SUNKEN
        self.__buttons[x.destination].update_idletasks()
        time.sleep(1)

        self.__refreshMove(x)

        self.__buttons[x.ini]['relief'] = Tkinter.RAISED
        self.__buttons[x.destination]['relief'] = Tkinter.RAISED
        self.__buttons[x.ini]['command'] = self.__click(x.ini)
        self.__buttons[x.destination]['command'] = self.__nothing


    def __refreshEat(self, way):
        t = self.__images[way[0].ini]['file']
        self.__images[way[0].ini]['file'] = "lib/images/empty.gif"
        self.__buttons[way[0].ini].update_idletasks()

        if not self.game.gameboard.emptyDarkQueen(way[-1].destination):
            self.__images[way[-1].destination]['file'] = "lib/images/darkqueen.gif"
        elif not self.game.gameboard.emptyLightQueen(way[-1].destination):
            self.__images[way[-1].destination]['file'] = "lib/images/lightqueen.gif"
        else:
            self.__images[way[-1].destination]['file'] = t

        self.__buttons[way[-1].destination].update_idletasks()

        for w in way:
            self.__images[w.between]['file'] = "lib/images/empty.gif"
            self.__buttons[w.between].update_idletasks()
            self.__buttons[w.between]['command'] = self.__click(w.between)


    def __refreshEatWithAnimation(self, way):
        wayLength = len(way)
        i = 0
        self.__buttons[way[0].ini]['relief'] = Tkinter.SUNKEN
        self.__buttons[way[0].ini].update_idletasks()
        while i < wayLength:
            time.sleep(1)
            self.__buttons[way[i].destination]['relief'] = Tkinter.SUNKEN
            self.__buttons[way[i].destination].update_idletasks()
            i += 1

        time.sleep(1)

        self.__refreshEat(way)

        i = 0
        self.__buttons[way[0].ini]['relief'] = Tkinter.RAISED
        while i < wayLength:
            self.__buttons[way[i].destination]['relief'] = Tkinter.RAISED
            i += 1
        self.__buttons[way[0].ini]['command'] = self.__click(way[0].ini)
        self.__buttons[way[-1].destination]['command'] = self.__nothing


    def __refreshBoard(self, x):
        if isinstance(x, AMove.AMove):
            self.__refreshMoveWithAnimation(x)
        else:
            self.__refreshEatWithAnimation(x)


    def __playMachine(self):
        if self.game.canPlay(not self.game.userPlayDarks):
            label = Tkinter.Label(self.parent, text="Thinking...")
            label.pack()
            self.parent.update_idletasks()
            x = self.game.FindNextMove()
            label.destroy()
            self.parent.update_idletasks()
            self.__refreshBoard(x)
            if not self.game.canPlay(self.game.userPlayDarks):
                tkMessageBox.showinfo("Game over", "You lose")
        else:
            tkMessageBox.showinfo("Game over", "You win!")


    def __doMove(self, i, destination, movePiece, moveQueen, eatOperator, nEatOperator):
        nEatPosibilitiesCount = nEatOperator.posibilitiesCount(self.game.gameboard)
        eatPosibilitiesCount = eatOperator.posibilitiesCount(self.game.gameboard)
        board = movePiece(i, destination, self.game.gameboard)
        if board:
            if nEatPosibilitiesCount == 0 and eatPosibilitiesCount > 0:
                tkMessageBox.showerror("Invalid movement", "You must capture because you are not threatened")
                self.__buttons[self.__ini]["relief"] = Tkinter.RAISED
                self.__buttons[self.__ini].update_idletasks()
                self.__ini = None
            else:
                self.game.gameboard = board
                self.__refreshMove( AMove.AMove(i, destination) )
                self.__buttons[self.__ini]["relief"] = Tkinter.RAISED
                self.__buttons[self.__ini].update_idletasks()
                self.__ini = None
                self.__playMachine()
        else:
            board = moveQueen(i, destination, self.game.gameboard)
            if board:
                if nEatPosibilitiesCount == 0 and eatPosibilitiesCount > 0:
                    tkMessageBox.showerror("Invalid movement", "You must capture because you are not threatened")
                    self.__buttons[self.__ini]["relief"] = Tkinter.RAISED
                    self.__buttons[self.__ini].update_idletasks()
                    self.__ini = None
                else:
                    self.game.gameboard = board
                    self.__refreshMove( AMove.AMove(i, destination) )
                    self.__buttons[self.__ini]["relief"] = Tkinter.RAISED
                    self.__buttons[self.__ini].update_idletasks()
                    self.__ini = None
                    self.__playMachine()
            else:
                return False

        return True


    def __markBeginOfEating(self, i, eatOperator):

        self.__buttons[i]["relief"] = Tkinter.SUNKEN

        self.__eatMoves.append(self.__ini)
        self.__eatMoves.append(i)

        self.__eatButton = Tkinter.Button(self.parent, text = "Capture!", command = self.__doEat(eatOperator))
        self.__eatButton.pack()


    def __doEat(self, eatOperator):
        def __eat():
            ok= True
            eatMovesLength = len(self.__eatMoves)
            ways = eatOperator.applyOperator(self.game.gameboard)
            if not ways.next() or eatOperator.waylength != eatMovesLength - 1:
                ok = False
            if ok:
                board = eatOperator.applyEat(self.__eatMoves, self.game.userPlayDarks, self.game.gameboard)
                if board:
                    for w, x in ways:
                        if x == board:
                            self.__refreshEat(w)
                            self.game.gameboard = x
                            break
                else:
                    ok = False

            for i in self.__eatMoves:
                self.__buttons[i]["relief"] = Tkinter.RAISED
                self.__buttons[i].update_idletasks()
            self.__eatMoves = []
            self.__ini = None
            self.__eatButton.destroy()
            self.parent.update_idletasks()

            if not ok:
                tkMessageBox.showerror("Invalid movement", "Please, make a valid movement")
            else:
                self.__playMachine()

            return ok

        return __eat


    def __refreshPieces(self, i, movePiece, moveQueen, eatOperator, nEatOperator):
        if len(self.__eatMoves) == 0:
            if self.__ini != None:
                if ( not self.__doMove(self.__ini, i, movePiece, moveQueen, eatOperator, nEatOperator) ):
                    self.__markBeginOfEating(i, eatOperator)
                    return
            else:
                if not self.game.gameboard.empty(i):
                    self.__ini = i
                    self.__buttons[i]["relief"] = Tkinter.SUNKEN
        else:
            self.__eatMoves.append(i)
            self.__buttons[i]["relief"] = Tkinter.SUNKEN


    def __click(self, i):
        def __clicked():
            if self.game.userPlayDarks:
                self.__refreshPieces(i,
                                     self.game.operatorMoveForDark._moveDarkPieceUser,
                                     self.game.operatorMoveForDark._moveDarkQueenUser,
                                     self.game.operatorEatForDark, self.game.operatorEatForLight)
            else:
                self.__refreshPieces(i,
                                     self.game.operatorMoveForLight._moveLightPieceUser,
                                     self.game.operatorMoveForLight._moveLightQueenUser,
                                     self.game.operatorEatForLight, self.game.operatorEatForDark)

        return __clicked


    def __nothing(self):
        pass


    def setGraphicalBoard( self, userPlayDarks = True ):
        gameboard = self.game.gameboard
#        gameboard.darkQueens = 1048576
#        gameboard.darkQueensCount = 1
#        gameboard.lightQueens = 0
#        gameboard.lightQueensCount = 0
#        gameboard.darkPieces = 0
#        gameboard.darkPiecesCount = 0
#        gameboard.lightPieces = 69215232
#        gameboard.lightPiecesCount = 4
        if userPlayDarks:
            k = gameboard.placesCount-1
        else:
            k = 0
        i = 0; kk = gameboard.dimension * gameboard.dimension - 1
        self.__images = []; self.__images = range(0, gameboard.placesCount); self.__buttons = range(0, gameboard.placesCount)
        brest = True; rest = { True: 0, False: 1 }

        while i < gameboard.dimension:
            frame = Tkinter.Frame(self.parent)
            frame.pack(side = Tkinter.TOP, anchor = Tkinter.W)
            j = 0
            while j < gameboard.dimension:
                image = Tkinter.PhotoImage(file = "lib/images/nothing.gif")
                button = Tkinter.Button(
                             frame, height = 36, width = 36,
                             command = self.__nothing,
                             image = image
                        )
                if kk % 2 == rest[brest]:
                    self.__images[k] = Tkinter.PhotoImage(file = "lib/images/nothing.gif")
                    self.__buttons[k] = Tkinter.Button(
                                             frame, height = 36, width = 36,
                                             command = self.__click(k),
                                             image = self.__images[k]
                                        )
                    button = self.__buttons[k]
                    if not gameboard.emptyDarkPiece(k):
                        if not self.game.userPlayDarks:
                            self.__buttons[k]["command"] = self.__nothing
                        self.__images[k]["file"] = "lib/images/dark.gif"
                    elif not gameboard.emptyLightPiece(k):
                        if self.game.userPlayDarks:
                            self.__buttons[k]["command"] = self.__nothing
                        self.__images[k]["file"] = "lib/images/light.gif"
                    elif not gameboard.emptyDarkQueen(k):
                        if not self.game.userPlayDarks:
                            self.__buttons[k]["command"] = self.__nothing
                        self.__images[k]["file"] = "lib/images/darkqueen.gif"
                    elif not gameboard.emptyLightQueen(k):
                        if self.game.userPlayDarks:
                            self.__buttons[k]["command"] = self.__nothing
                        self.__images[k]["file"] = "lib/images/lightqueen.gif"
                    else:
                        self.__images[k]["file"] = "lib/images/empty.gif"
                    if userPlayDarks:
                        k -= 1
                    else:
                        k += 1

                button.pack(side = Tkinter.LEFT)
                j += 1
                kk -= 1
            i += 1
            brest = not brest
        if not self.game.userPlayDarks:
            self.__playMachine()
