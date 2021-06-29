# -*- coding: UTF-8 -*-
'''
@author: Ernesto Soto Gómez
'''

import Singleton, Tkinter, Game, GraphicalBoard, Gameboard

class UserInterface(Singleton.Singleton):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__game = None
        self.__graphicalBoard = GraphicalBoard.GraphicalBoard()
        self.__root =  Tkinter.Tk()
        self.__initialize()
        self.__root.mainloop()


    def __initialize(self):
        self.__root.title("Checkers")
        self.__root.minsize ( width=300, height=300 )

        self.__menuFrame = Tkinter.Frame(self.__root)
        self.__menuFrame.pack(anchor = Tkinter.W)

        self.__juegoMenubutton = Tkinter.Menubutton( self.__menuFrame, text = "Game", relief = Tkinter.GROOVE )

        self.__juegoMenubutton.pack( side = Tkinter.LEFT )

        self.__juegoMenu = Tkinter.Menu( self.__juegoMenubutton, tearoff = 0 )

        self.__juegoMenubutton["menu"] = self.__juegoMenu

        self.__juegoMenu.add_command( label = "New game", command = self.__juegoNuevo )

        self.__juegoMenu.add_command( label = "Exit", command = self.__salir )

        self.__ayudaMenubutton = Tkinter.Menubutton( self.__menuFrame, text = "Help", relief = Tkinter.GROOVE )

        self.__ayudaMenubutton.pack( side = Tkinter.LEFT )

        self.__ayudaMenu = Tkinter.Menu( self.__ayudaMenubutton, tearoff = 0 )

        self.__ayudaMenubutton["menu"] = self.__ayudaMenu

        self.__ayudaMenu.add_command( label = "Rules", command = self.__reglas )

        self.__ayudaMenu.add_command(label = "About", command = self.__acercaDe )

        self.__boardFrame = Tkinter.Frame(self.__root, relief = Tkinter.SUNKEN)
        self.__boardFrame["borderwidth"] = 1
        self.__boardFrame.pack( pady = 10 )

    def __resetBoardFrame(self):
        self.__boardFrame.destroy()
        self.__root.update_idletasks()
        self.__boardFrame = Tkinter.Frame(self.__root, relief = Tkinter.SUNKEN)
        self.__boardFrame["borderwidth"] = 1
        self.__boardFrame.pack( pady = 10 )

    def __juegoNuevo(self):
        self.__resetBoardFrame()
        self.__optionsFrame = Tkinter.Frame(self.__boardFrame)
        self.__optionsFrame.pack()
        self.__gameTypeLabelFrame = Tkinter.LabelFrame(self.__optionsFrame, text = "Select board type")
        self.__gameTypeLabelFrame.pack(side = Tkinter.LEFT, anchor = Tkinter.NW, padx = 10, pady = 10)
        self.__gameType = Tkinter.StringVar()
        self.__gameTypeTraditionalRadioButton = Tkinter.Radiobutton( self.__gameTypeLabelFrame,
                                                                     text = "Traditional",
                                                                     variable = self.__gameType,
                                                                     value = "traditional" )
        self.__gameTypeTraditionalRadioButton.pack(padx = 10, pady = 10, anchor = Tkinter.NW)
        self.__gameTypeTraditionalRadioButton.select()
        self.__gameTypeInternationalRadioButton = Tkinter.Radiobutton( self.__gameTypeLabelFrame,
                                                                       text = "International",
                                                                       variable = self.__gameType,
                                                                       value = "international" )
        self.__gameTypeInternationalRadioButton.pack(padx = 10, pady = 10, anchor = Tkinter.NW)
        self.__gameTypeReducedRadioButton = Tkinter.Radiobutton( self.__gameTypeLabelFrame,
                                                                 text = "Reduced international",
                                                                 variable = self.__gameType,
                                                                 value = "reduced" )
        self.__gameTypeReducedRadioButton.pack(padx = 10, pady = 10, anchor = Tkinter.NW)

        self.__userPlaysLabelFrame = Tkinter.LabelFrame(self.__optionsFrame, text = "Select party")
        self.__userPlaysLabelFrame.pack(side = Tkinter.LEFT, anchor = Tkinter.NW, padx = 10, pady = 10)
        self.__userPlays = Tkinter.StringVar()
        self.__userPlaysDarkRadioButton = Tkinter.Radiobutton( self.__userPlaysLabelFrame,
                                                                text = "Darks",
                                                                variable = self.__userPlays,
                                                                value = "darks" )
        self.__userPlaysDarkRadioButton.pack(padx = 10, pady = 10, anchor = Tkinter.NW)
        self.__userPlaysDarkRadioButton.select()
        self.__userPlaysLightRadioButton = Tkinter.Radiobutton( self.__userPlaysLabelFrame,
                                                                text = "Lights",
                                                                variable = self.__userPlays,
                                                                value = "lights" )
        self.__userPlaysLightRadioButton.pack(padx = 10, pady = 10, anchor = Tkinter.NW)

        self.__buttonOk = Tkinter.Button(self.__boardFrame, text = "OK", command = self.__aceptarJuego)
        self.__buttonOk.pack(padx = 10, pady = 10)



    def __aceptarJuego(self):
        if self.__userPlays.get() == "darks":
            _userPlayDarks = True
        else:
            _userPlayDarks = False

        if self.__gameType.get() == "traditional":
            _dimension = 8
            _piecesCount = 12
            _maxDepth = 5
        elif self.__gameType.get() == "international":
            _dimension = 10
            _piecesCount = 20
            _maxDepth = 4
        else:
            _dimension = 10
            _piecesCount = 15
            _maxDepth = 4

        self.__game = Game.Game( dimension = _dimension, piecesCount = _piecesCount,
                                 userPlayDarks = _userPlayDarks, maxDepth = _maxDepth )
        self.__graphicalBoard.game = self.__game
        self.__resetBoardFrame()
        self.__graphicalBoard.parent = self.__boardFrame
        self.__graphicalBoard.setGraphicalBoard(userPlayDarks = _userPlayDarks)

    def __salir(self):
        self.__root.quit()

    def __acercaDe(self):
        self.__resetBoardFrame()
        self.__autorLabelFrame = Tkinter.LabelFrame(self.__boardFrame, text = "Checkers")
        self.__autorLabelFrame.pack(side = Tkinter.TOP, anchor = Tkinter.NW, padx = 10, pady = 10)
        self.autorLabel = Tkinter.Label(self.__autorLabelFrame,
                              text = '''Version 0.1
by Ernesto Soto Gómez
(gmail: esto.yinyang)
''', font = ("Courier", 12, "bold italic"))
        self.autorLabel.pack(anchor = Tkinter.CENTER, padx = 10, pady = 10)
        self.autorCanvas = Tkinter.Canvas(self.__autorLabelFrame, width = 200, height = 161)
        self.autorCanvas.pack(padx = 10, pady = 10)
        self.autorImage = Tkinter.PhotoImage(file = "lib/images/autor.gif")
        self.autorCanvas.create_image(0, 0, image = self.autorImage, anchor = Tkinter.NW)

    def __ayuda(self):
        pass

    def __reglas(self):
        pass
