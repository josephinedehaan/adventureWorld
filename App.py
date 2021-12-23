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

        self.frame1 = tk.Frame(root, width=600, height=250, bg='WHITE', borderwidth=2)
        self.frame1.pack_propagate(0)   # Prevents resizing
        self.frame2 = tk.Frame(root, width=400, height=150, bg='LIGHt GREY', borderwidth=2)
        self.frame2.grid_propagate(0)   # Prevents resizing
        # This packs both frames into the root window ...
        self.frame1.pack()
        self.frame2.pack()

        # Now add some useful widgets ...
        self.textArea1 = tk.Label(self.frame1, text=self.game.printWelcome(), wraplength=600)
        self.textArea1.pack()
        self.cmdArea = tk.Entry(self.frame2, text='')
        self.cmdArea.pack()
        self.buildGUI()

    def buildGUI(self):
        self.doCmd = tk.Button(self.frame2, text='Run command',
                               fg='black', bg='blue',
                               command=self.doCommand)
        self.doCmd.pack()
        self.textArea1.configure(text=self.game.printWelcome())

    def doCommand(self):
        command = self.cmdArea.get()  # Returns a 2-tuple
        self.processCommand(command)

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
        elif commandWord == "TALKTO":
            self.textArea1.configure(text=self.game.player.doSpeak(secondWord))
        elif commandWord == "TAKE":
            self.textArea1.configure(text=self.game.player.doTake(secondWord))
        elif commandWord == "LIST":
            self.textArea1.configure(text=self.game.player.doReadShoppingList())
        elif commandWord == "BASKET":
            self.game.player.doSeeBasket()
        elif commandWord == "COMPARE":
            self.game.player.doCompare()
        elif commandWord == "SCORE":
            self.game.player.doSeePoints()
        elif commandWord == "GUESS":
            self.game.player.doGuess(secondWord)
        elif commandWord == "TIME":
            self.game.player.doCheckTime()
        elif commandWord == "UNLOCK":
            self.game.createSecretRoom()
        elif commandWord == "TEST":
            self.game.player.test()
        elif commandWord == "QUIT":
            self.game.wantToQuit = True
        else:
            # Unknown command ...
            self.textArea1.configure(text="Don't know what you mean")

        return self.game.wantToQuit


def main():

    win = tk.Tk()                           # Create a window
    win.title("Adventure World with GUI")   # Set window title
    win.geometry("800x300")                 # Set window size
    win.resizable(False, False)             # Both x and y dimensions ...

    # Create the GUI as a Frame
    # and attach it to the window ...
    myApp = App(win)



    # Call the GUI mainloop ...
    win.mainloop()

if __name__ == "__main__":
    main()