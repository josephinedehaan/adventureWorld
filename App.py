import tkinter as tk
from Game import Game

class App:
    # Creates a Frame for the application
    # and populates the GUI ...
    def __init__(self, root):

        self.game = Game()

        # Create two frames owned by the window root
        # In order to use multiple layout managers, the frames
        # cannot share a parent frame. Here both frames are owned
        # by a top level instance root.

        self.textArea1 = tk.Label(text=self.game.printWelcome(), wraplength=600)
        self.textArea1.grid(row=9, column=2, rowspan=2, columnspan=2)
        self.entryBox = tk.Entry(text='')
        self.entryBox.grid(row=7, column=0)
        self.buildGUI()

    def buildGUI(self):
        self.doHelp = tk.Button(text='Help', fg='black', command=self.doHelp)
        self.doHelp.grid(row=0, column=0, columnspan=2)
        self.doLook = tk.Button(text='Look', fg='black', command=self.doLook)
        self.doLook.grid(row=1, column=0, columnspan=2)
        self.doSpeak = tk.Button(text='Speak', fg='black', command=self.doSpeak)
        self.doSpeak.grid(row=2, column=0, columnspan=2)
        self.doList = tk.Button(text='List', fg='black', command=self.doList)
        self.doList.grid(row=3, column=0, columnspan=2)
        self.doCompare = tk.Button(text='Compare', fg='black', command=self.doCompare)
        self.doCompare.grid(row=4, column=0, columnspan=2)
        self.doUnlock = tk.Button(text='Unlock', fg='black', command=self.doUnlock)
        self.doUnlock.grid(row=5, column=0, columnspan=2)
        self.doQuit = tk.Button(text='Quit', fg='black')    # functionality needs to be implemented
        self.doQuit.grid(row=6, column=0, columnspan=2)     # program quits if i put exit() as command, look up!



        self.runCommand = tk.Button(text='Run command', fg='purple', bd=1, command=self.doCommand)
        self.runCommand.grid(row=8, column=0)


        self.goNorth = tk.Button(text='Go North ^', fg='black', command=self.doGoNorth)
        self.goNorth.grid(row=9, column=0, columnspan=2)

        self.goSouth = tk.Button(text='Go South', fg='black', command=self.doGoSouth)
        self.goSouth.grid(row=10, column=0, columnspan=2)

        self.goEast = tk.Button(text='Go East >', fg='black', command=self.doGoEast)
        self.goEast.grid(row=9, column=4, columnspan=2)

        self.goWest = tk.Button(text='Go West <', fg='black', command=self.doGoWest)
        self.goWest.grid(row=10, column=4, columnspan=2)


        self.textArea1.configure(text=self.game.printWelcome())

    def doCommand(self):
        command = self.entryBox.get()  # Returns a 2-tuple
        self.processCommand(command)

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

    def doGoNorth(self):
        x = self.game.player.doGoCommand('NORTH')
        self.textArea1.configure(text=x)

    def doGoSouth(self):
        x = self.game.player.doGoCommand('SOUTH')
        self.textArea1.configure(text=x)

    def doGoEast(self):
        x = self.game.player.doGoCommand('EAST')
        self.textArea1.configure(text=x)

    def doGoWest(self):
        x = self.game.player.doGoCommand('WEST')
        self.textArea1.configure(text=x)



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
    win.geometry("900x400")                 # Set window size
    win.resizable(False, False)             # Both x and y dimensions ...

    # Create the GUI as a Frame
    # and attach it to the window ...
    myApp = App(win)



    # Call the GUI mainloop ...
    win.mainloop()

if __name__ == "__main__":
    main()