import tkinter as tk
from Game import Game
from PIL import ImageTk, Image


class App:
    def __init__(self, root):
        self.game = Game()

        # Text area where all text is printed
        self.textArea1 = tk.Label(text=self.game.printWelcome(), width=44, height=8, borderwidth=1, relief='solid',
                                  bg='light grey', fg='black', wraplength=400, justify='center')
        self.textArea1.grid(row=10, column=2, rowspan=3, columnspan=2, sticky='s')

        # Entry box for the guss and take commands
        self.entryBox = tk.Entry(text='', width=2)
        self.entryBox.grid(row=10, column=0, columnspan=2, sticky='sew')

        # Image area
        self.outsidePic = ImageTk.PhotoImage(Image.open("outside.jpeg"))
        self.pictureArea = tk.Label(image=self.outsidePic)
        self.pictureArea.grid(row=2, column=2, rowspan=8, columnspan=2, sticky='nsew')

        # Score area
        self.scoreArea = tk.Label(text=" Your score: 0", width=22, bg='light grey', fg='black', anchor='w',
                                  justify='left', borderwidth=1, relief='solid')
        self.scoreArea.grid(row=0, column=3)

        # Current Room area
        self.locationArea = tk.Label(text="Outside. Possible directions: NORTH", width=44, bg='light grey', fg='black',
                                     borderwidth=1, relief='solid')
        self.locationArea.grid(row=1, column=2, columnspan=2, sticky='nsew')

        # Basket area
        self.basketframe = tk.LabelFrame(text="Your Basket")
        self.basketframe.grid(row=2, column=4, rowspan=7, columnspan=3, sticky='nsew')
        self.basketArea = tk.Label(self.basketframe, wraplength=100, text="", anchor='w', justify='left')
        self.basketArea.grid()

        # Initialises GUI widgets
        self.buildGUI()

    def buildGUI(self):
        self.doHelp = tk.Button(text='HELP', fg='black', width=5, command=self.doHelp)
        self.doHelp.grid(row=0, column=0, columnspan=2, sticky='s')
        self.doQuit = tk.Button(text='QUIT', width=10, fg='red')  # functionality needs to be implemented
        self.doQuit.grid(row=0, column=4, columnspan=3)  # program quits if i put exit() as command, look up!

        # Command Buttons
        self.speakIcon = ImageTk.PhotoImage(Image.open('speak.png'))
        self.listIcon = ImageTk.PhotoImage(Image.open('list.png'))
        self.unlockIcon = ImageTk.PhotoImage(Image.open('unlock.png'))

        self.doSpeak = tk.Button(image=self.speakIcon, command=self.doSpeak)
        self.doSpeak.grid(row=3, column=0, columnspan=2, sticky='s')
        self.doCompare = tk.Button(image=self.listIcon, command=self.doCompare)
        self.doCompare.grid(row=4, column=0, columnspan=2, sticky='s')
        self.doUnlock = tk.Button(image=self.unlockIcon, command=self.doUnlock)
        self.doUnlock.grid(row=5, column=0, columnspan=2, sticky='s')


        self.Take = tk.Button(text='Take', fg='black', width=2, command=self.doTake)
        self.Take.grid(row=11, column=0, columnspan=1, stick='new')
        self.guess = tk.Button(text='Guess', fg='black', width=2, command=self.doGuess)
        self.guess.grid(row=11, column=1, columnspan=1, sticky='new')

        # Direction buttons
        self.northIcon = ImageTk.PhotoImage(Image.open('north.png'))
        self.southIcon = ImageTk.PhotoImage(Image.open('south.png'))
        self.eastIcon = ImageTk.PhotoImage(Image.open('east.png'))
        self.westIcon = ImageTk.PhotoImage(Image.open('west.png'))
        self.midIcon = ImageTk.PhotoImage(Image.open('middle.png'))
        self.goNorth = tk.Button(image=self.northIcon, command=self.doGoNorth, width=20)
        self.goNorth.grid(row=10, column=5, sticky='nsew')
        self.goSouth = tk.Button(image=self.southIcon, command=self.doGoSouth)
        self.goSouth.grid(row=12, column=5, sticky='nsew')
        self.middle = tk.Label(image=self.midIcon, command=None)
        self.middle.grid(row=11, column=5, sticky='nsew')
        self.goEast = tk.Button(image=self.eastIcon, command=self.doGoEast)
        self.goEast.grid(row=11, column=6, sticky='nsew')
        self.goWest = tk.Button(image=self.westIcon, command=self.doGoWest)
        self.goWest.grid(row=11, column=4, sticky='nsew')

        # Timer and score counter display
        self.timerArea = tk.Label(text=" " + self.game.player.doCheckTime(), width=22, bg='light grey', fg='black',
                                  anchor='w', justify='left', borderwidth=1, relief='solid')
        self.timerArea.grid(row=0, column=2)

        # Welcome message
        self.textArea1.configure(text=self.game.printWelcome())

    def scoreCounter(self):
        score = self.game.player.doSeePoints()
        self.scoreArea.configure(text=score)

    def doTake(self):
        item = self.entryBox.get()
        basket = self.game.player.basket
        self.processCommand('TAKE ' + item)
        self.basketArea.configure(text=basket)
        self.scoreCounter()

    def doGuess(self):
        item = self.entryBox.get()
        basket = self.game.player.basket
        self.processCommand('GUESS ' + item)
        self.scoreCounter()
        self.basketArea.configure(text=basket)



    def doHelp(self):
        x = self.game.doPrintHelp()
        self.textArea1.configure(text=x)

    def doLook(self):
        x = self.game.player.doLookAround()
        self.textArea1.configure(text=x)

    def doSpeak(self):
        x = self.game.player.doSpeak()
        self.textArea1.configure(text=x)

    def doList(self):
        x = self.game.player.doReadShoppingList()
        self.textArea1.configure(text=x)

    def doCompare(self):
        y = self.game.player.doReadShoppingList()
        x = self.game.player.doCompare()
        self.textArea1.configure(text=f'Your list: {y} \n {x}')

    def doUnlock(self):
        x = self.game.createSecretRoom()
        self.textArea1.configure(text=x)

    # Directions
    def doGoNorth(self):
        x = self.game.player.doGoCommand('NORTH')
        self.locationArea.configure(text=x)
        self.textArea1.configure(text=self.game.player.doLookAround())

        self.changeImage()

    def doGoSouth(self):
        x = self.game.player.doGoCommand('SOUTH')
        self.locationArea.configure(text=x)
        self.textArea1.configure(text=self.game.player.doLookAround())
        self.changeImage()

    def doGoEast(self):
        x = self.game.player.doGoCommand('EAST')
        self.locationArea.configure(text=x)
        self.textArea1.configure(text=self.game.player.doLookAround())
        self.changeImage()

    def doGoWest(self):
        x = self.game.player.doGoCommand('WEST')
        self.locationArea.configure(text=x)
        self.textArea1.configure(text=self.game.player.doLookAround())
        self.changeImage()

    def changeImage(self):
        self.lobbyPic = ImageTk.PhotoImage(Image.open("lobby.jpg"))
        self.aisle1Pic = ImageTk.PhotoImage(Image.open("aisle_1.jpg"))
        self.aisle2Pic = ImageTk.PhotoImage(Image.open("aisle_2.jpg"))
        self.aisle3Pic = ImageTk.PhotoImage(Image.open("aisle_3.jpg"))
        self.aisle4Pic = ImageTk.PhotoImage(Image.open("aisle_4.jpg"))
        self.aisle5Pic = ImageTk.PhotoImage(Image.open("aisle_5.jpg"))
        # self.aisle6Pic = ImageTk.PhotoImage(Image.open())
        self.checkoutPic = ImageTk.PhotoImage(Image.open("checkout.jpg"))

        if self.game.player.currentRoom == self.game.lobby:
            self.pictureArea.configure(image=self.lobbyPic)
        elif self.game.player.currentRoom == self.game.outside:
            self.pictureArea.configure(image=self.outsidePic)
        elif self.game.player.currentRoom == self.game.aisleOne:
            self.pictureArea.configure(image=self.aisle1Pic)
        elif self.game.player.currentRoom == self.game.aisleTwo:
            self.pictureArea.configure(image=self.aisle2Pic)
        elif self.game.player.currentRoom == self.game.aisleThree:
            self.pictureArea.configure(image=self.aisle3Pic)
        elif self.game.player.currentRoom == self.game.aisleFour:
            self.pictureArea.configure(image=self.aisle4Pic)
        elif self.game.player.currentRoom == self.game.aisleFive:
            self.pictureArea.configure(image=self.aisle5Pic)
        # elif self.game.player.currentRoom == self.game.aisleSix:
        #     self.pictureArea.configure(image=self.aisle6Pic)
        elif self.game.player.currentRoom == self.game.checkout:
            self.pictureArea.configure(image=self.checkoutPic)

    def getCommandString(self, inputLine):
        """
            Fetches a command (borrowed from old TextUI)
        :return: a 2-tuple of the form (commandWord, secondWord)
        """
        word1 = None
        word2 = None
        if inputLine != "":
            allWords = inputLine.split()
            word1 = allWords[0]
            if len(allWords) > 1:
                word2 = allWords[1]
            else:
                word2 = None
            # Just ignore any other words
        return (word1, word2)

    def processCommand(self, command):
        """
            Process a command from the TextUI
        :param command: a 2-tuple of the form (commandWord, secondWord)
        :return: True if the game has been quit, False otherwise
        """
        commandWord, secondWord = self.getCommandString(command)
        if commandWord != None:
            commandWord = commandWord.upper()
        if secondWord != None:
            secondWord = secondWord.upper()

        if commandWord == "HELP":
            self.textArea1.configure(text=self.game.doPrintHelp())
        # elif commandWord == "GO":
        #     self.locationArea.configure(text=self.game.player.doGoCommand(secondWord))
        # elif commandWord == "LOOK":
        # #     self.textArea1.configure(text=self.game.player.doLookAround())
        # elif commandWord == "SPEAK":
        #     self.textArea1.configure(text=self.game.player.doSpeak())
        elif commandWord == "TAKE":
            self.textArea1.configure(text=self.game.player.doTake(secondWord))
        elif commandWord == "LIST":
            self.textArea1.configure(text=self.game.player.doReadShoppingList())
        elif commandWord == "BASKET":
            self.textArea1.configure(text=self.game.player.doSeeBasket())
        elif commandWord == "COMPARE":
            self.textArea1.configure(text=self.game.player.doCompare())
        elif commandWord == "SCORE":
            self.textArea1.configure(text=self.game.player.doSeePoints())
        elif commandWord == "GUESS":
            self.textArea1.configure(text=self.game.player.doGuess(secondWord))
        elif commandWord == "TIME":
            self.textArea1.configure(text=self.game.player.doCheckTime())
        elif commandWord == "UNLOCK":
            self.textArea1.configure(text=self.game.createSecretRoom())
        else:
            # Unknown command ...
            self.textArea1.configure(text="Don't know what you mean")


def main():
    win = tk.Tk()  # Create a window
    win.title("Adventure World with GUI")  # Set window title
    win.geometry("650x450")  # Set window size
    win.resizable(False, False)  # Both x and y dimensions ...

    App(win)

    win.mainloop()


if __name__ == "__main__":
    main()
