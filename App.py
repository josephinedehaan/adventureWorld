import tkinter as tk
from Game import Game
from PIL import ImageTk, Image

class App:
    def __init__(self, root):
        self.game = Game()

        # Text area where all text is printed
        self.textArea1 = tk.Label(text=self.game.printWelcome(), width=50, height=8,  borderwidth=1, relief='solid',
                                  bg='light grey', fg='black', wraplength=400, justify='center')
        self.textArea1.grid(row=9, column=2, rowspan=2, columnspan=2)

        # Entry box for the guss and take commands
        self.entryBox = tk.Entry(text='', width=2)
        self.entryBox.grid(row=7, column=0, columnspan=2, sticky='nsew')

        # Image area
        self.outsidePic = ImageTk.PhotoImage(Image.open("outside.jpeg"))
        self.pictureArea = tk.Label(image=self.outsidePic, height=10)
        self.pictureArea.grid(row=1, column=2, rowspan=8, columnspan=2, sticky='nsew')

        # Score area
        self.scoreArea = tk.Label(text="Your score: 0", width=25, bg='light grey', fg='black', anchor='w', justify='left')
        self.scoreArea.grid(row=0, column=3)

        # Basket area
        self.basketframe = tk.LabelFrame(text="Your Basket")
        self.basketframe.grid(row=1, column=4, rowspan=8, columnspan=2, sticky='nsew')
        self.basketArea = tk.Label(self.basketframe, wraplength=100, text="", anchor='w', justify='left')
        self.basketArea.grid()

        # Initialises GUI widgets
        self.buildGUI()

    def buildGUI(self):
        # Command Buttons
        self.doHelp = tk.Button(text='Help', fg='black', width=10, command=self.doHelp)
        self.doHelp.grid(row=0, column=0, columnspan=2, sticky='w')
        self.doLook = tk.Button(text='Look', fg='black', width=10, command=self.doLook)
        self.doLook.grid(row=1, column=0, columnspan=2, sticky='w')
        self.doSpeak = tk.Button(text='Speak', fg='black', width=10, command=self.doSpeak)
        self.doSpeak.grid(row=2, column=0, columnspan=2, sticky='w')
        self.doList = tk.Button(text='List', fg='black', width=10, command=self.doList)
        self.doList.grid(row=3, column=0, columnspan=2, sticky='w')
        self.doCompare = tk.Button(text='Compare', relief='raised', fg='black', width=10, command=self.doCompare)
        self.doCompare.grid(row=4, column=0, columnspan=2, sticky='w')
        self.doUnlock = tk.Button(text='Unlock', fg='black', width=10, command=self.doUnlock)
        self.doUnlock.grid(row=5, column=0, columnspan=2, sticky='w')

        self.doQuit = tk.Button(text='Quit', width=10, fg='black')            # functionality needs to be implemented
        self.doQuit.grid(row=0, column=4, columnspan=2, sticky='w')                             # program quits if i put exit() as command, look up!

        self.Take = tk.Button(text='Take', fg='black', width=2, command=self.doTake)
        self.Take.grid(row=8, column=0, columnspan=1, stick='nsew')
        self.guess = tk.Button(text='Guess', fg='black', width=2, command=self.doGuess)
        self.guess.grid(row=8, column=1,columnspan=1, sticky='nsew')

        # Direction buttons
        self.goNorth = tk.Button(text='↑', fg='black', width=10, command=self.doGoNorth)
        self.goNorth.grid(row=9, column=0, columnspan=2, sticky='s')
        self.goSouth = tk.Button(text='↓', fg='black', width=10, command=self.doGoSouth)
        self.goSouth.grid(row=10, column=0, columnspan=2, sticky='n')
        self.goEast = tk.Button(text='→', fg='black', width=10, command=self.doGoEast)
        self.goEast.grid(row=9, column=4, columnspan=2, sticky='s')
        self.goWest = tk.Button(text='←', fg='black', width=10, command=self.doGoWest)
        self.goWest.grid(row=10, column=4, columnspan=2, sticky='n')

        # Timer and score counter display
        self.timerArea = tk.Label(text=self.game.player.doCheckTime(), width=25, bg='pink', fg='black')
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
        self.processCommand('GUESS ' + item)

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
        x = self.game.player.doCompare()
        self.textArea1.configure(text=x)

    def doUnlock(self):
        x = self.game.createSecretRoom()
        self.textArea1.configure(text=x)

    # Directions
    def doGoNorth(self):
        x = self.game.player.doGoCommand('NORTH')
        self.textArea1.configure(text=x)
        self.changeImage()

    def doGoSouth(self):
        x = self.game.player.doGoCommand('SOUTH')
        self.textArea1.configure(text=x)
        self.changeImage()


    def doGoEast(self):
        x = self.game.player.doGoCommand('EAST')
        self.textArea1.configure(text=x)
        self.changeImage()


    def doGoWest(self):
        x = self.game.player.doGoCommand('WEST')
        self.textArea1.configure(text=x)
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
        elif commandWord == "GO":
            self.textArea1.configure(text=self.game.player.doGoCommand(secondWord))
        elif commandWord == "LOOK":
            self.textArea1.configure(text=self.game.player.doLookAround())
        elif commandWord == "SPEAK":
            self.textArea1.configure(text=self.game.player.doSpeak())
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

    win = tk.Tk()                           # Create a window
    win.title("Adventure World with GUI")   # Set window title
    win.geometry("720x400")                 # Set window size
    win.resizable(False, False)             # Both x and y dimensions ...

    App(win)

    win.mainloop()


if __name__ == "__main__":
    main()
