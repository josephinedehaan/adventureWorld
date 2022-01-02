import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from Game import Game
import time
import os
import sys

"""
    Class Description
"""


class App:
    def __init__(self, root):
        self.game = Game()
        self.buildGUI()
        self.updateClock()

    def buildGUI(self):
        """
            Description.
        :param: None
        :return: None
        """
        # Text area where all text is printed
        self.textArea1 = tk.Label(text=self.game.printWelcome(), width=44, height=8, borderwidth=1, relief='solid',
                                  bg='light grey', fg='black', wraplength=400, justify='center')
        self.textArea1.grid(row=10, column=2, rowspan=3, columnspan=2, sticky='s')

        # Image area
        self.outsidePic = ImageTk.PhotoImage(Image.open("outside.jpeg"))
        self.pictureArea = tk.Label(image=self.outsidePic)
        self.pictureArea.grid(row=2, column=2, rowspan=8, columnspan=2, sticky='nsew')

        # Timer and score counter display
        self.timerArea = tk.Label(text="", width=22, bg='light grey', fg='black',
                                  anchor='w', justify='left', borderwidth=1, relief='solid')
        self.scoreArea = tk.Label(text=" Your score: 0", width=22, bg='light grey', fg='black', anchor='w',
                                  justify='left', borderwidth=1, relief='solid')
        self.timerArea.grid(row=0, column=2)
        self.scoreArea.grid(row=0, column=3)

        # Current Room area
        self.locationArea = tk.Label(text="Outside. Possible directions: NORTH", width=44, bg='light pink', fg='black',
                                     borderwidth=1, relief='solid')
        self.locationArea.grid(row=1, column=2, columnspan=2, sticky='nsew')

        # Basket area
        self.basketframe = tk.LabelFrame(text="Your Basket")
        self.basketframe.grid(row=2, column=4, rowspan=7, columnspan=3, sticky='nsew')
        self.basketArea = tk.Label(self.basketframe, wraplength=100, text="", anchor='w', justify='left')
        self.basketArea.grid()

        # Help and Quit buttons
        self.doHelp = tk.Button(text='HELP', fg='black', width=5, command=self.doHelp)
        self.doHelp.grid(row=0, column=0, columnspan=2, sticky='s')
        self.doQuit = tk.Button(text='QUIT', width=10, fg='red', command=self.quitPopUp)
        self.doQuit.grid(row=0, column=4, columnspan=3)

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

        # Take and Guess Entry and buttons
        self.entryBox = tk.Entry(text='', width=2)
        self.entryBox.grid(row=10, column=0, columnspan=2, sticky='sew')
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

    def updateClock(self):
        """
            Updates timer every second.
        :param: None
        :return: None
        """
        self.timerArea.configure(text=" " + self.game.player.doCheckTime())
        self.timerArea.after(1000, self.updateClock)

    def doSpeak(self):
        """
            Fetches dialogue and updates text area.
        :param: None
        :return: None
        """
        x = self.game.player.doSpeak()
        self.textArea1.configure(text=x)
        self.scoreCounter()

    def scoreCounter(self):
        """
            Fetches score and configures score area.
        :param: None
        :return: None
        """
        score = self.game.player.doSeePoints()
        self.scoreArea.configure(text=score)

    def doTake(self):
        """
            Gets .
        :param: None
        :return: None
        """
        item = self.entryBox.get()
        basket = self.game.player.basket
        self.processTypedCommand('TAKE ' + item)
        self.basketArea.configure(text=basket)
        self.scoreCounter()
        self.entryBox.delete(0, 'end')

    def doGuess(self):
        """
            Description.
        :param: None
        :return: None
        """
        item = self.entryBox.get()
        basket = self.game.player.basket
        self.processTypedCommand('GUESS ' + item)
        self.scoreCounter()
        self.basketArea.configure(text=basket)
        self.entryBox.delete(0, 'end')


    def doHelp(self):
        """
            Description.
        :param: None
        :return: None
        """
        x = self.game.doPrintHelp()
        self.textArea1.configure(text=x)


    def doCompare(self):
        """
            Description.
        :param: None
        :return: None
        """
        y = self.game.player.doReadShoppingList()
        x = self.game.player.doCompare()
        self.textArea1.configure(text=f'Your list: {y} \n {x}')

    def doUnlock(self):
        """
            Description.
        :param: None
        :return: None
        """
        x = self.game.createSecretRoom()
        self.textArea1.configure(text=x)

    def doLook(self):
        """
            Description.
        :param: None
        :return: None
        """
        x = self.game.player.currentRoom.description
        self.textArea1.configure(text=x)

    def doGoNorth(self):
        """
            Description.
        :param: None
        :return: None
        """
        x = self.game.player.doGoCommand('NORTH')
        self.locationArea.configure(text=x)
        self.doLook()
        self.changeImage()

    def doGoSouth(self):
        """
            Description.
        :param: None
        :return: None
        """
        x = self.game.player.doGoCommand('SOUTH')
        self.locationArea.configure(text=x)
        self.doLook()
        self.changeImage()

    def doGoEast(self):
        """
            Description.
        :param: None
        :return: None
        """
        x = self.game.player.doGoCommand('EAST')
        self.locationArea.configure(text=x)
        self.doLook()
        self.changeImage()

    def doGoWest(self):
        """
            Description.
        :param: None
        :return: None
        """
        x = self.game.player.doGoCommand('WEST')
        self.locationArea.configure(text=x)
        self.doLook()
        self.changeImage()

    def quitPopUp(self):
        """
            Description.
        :param: None
        :return: None
        """
        quitResponse = messagebox.askyesno('Quit', 'Are you sure you want to quit??')
        if quitResponse == 1:
            quit()

    def endGame(self):
        """
            Description.
        :param: None
        :return: None
        """
        message = self.game.player.doCheckOut()

        time.sleep(1000)

        if self.game.player.checkOutAllowed and self.game.player.currentRoom is self.game.checkout:
            response = messagebox.askyesno('Congratulations', message + '\n Would you like to play again?')
            if response == 0:
                quit()
            else:
                self.playAgain()

    def playAgain(self):
        """
            Description.
        :param: None
        :return: None
        """
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

    def changeImage(self):
        """
            Description.
        :param: None
        :return: None
        """
        self.lobbyPic = ImageTk.PhotoImage(Image.open("lobby.jpg"))
        self.aisle1Pic = ImageTk.PhotoImage(Image.open("aisle_1.jpg"))
        self.aisle2Pic = ImageTk.PhotoImage(Image.open("aisle_2.jpg"))
        self.aisle3Pic = ImageTk.PhotoImage(Image.open("aisle_3.jpg"))
        self.aisle4Pic = ImageTk.PhotoImage(Image.open("aisle_4.jpg"))
        self.aisle5Pic = ImageTk.PhotoImage(Image.open("aisle_5.jpg"))
        self.secretAislePic = ImageTk.PhotoImage(Image.open("secret_aisle.jpg"))
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
        elif self.game.player.currentRoom == self.game.secretAisle:
            self.pictureArea.configure(image=self.secretAislePic)
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
        return (word1, word2)

    def processTypedCommand(self, command):
        """
            Process a command from text entry for Guess and Take.
        :param command: a 2-tuple of the form (commandWord, secondWord)
        :return: True if the game has been quit, False otherwise
        """
        commandWord, secondWord = self.getCommandString(command)
        if commandWord != None:
            commandWord = commandWord.upper()
        if secondWord != None:
            secondWord = secondWord.upper()

        if commandWord == "TAKE":
            self.textArea1.configure(text=self.game.player.doTake(secondWord))
        elif commandWord == "GUESS":
            self.textArea1.configure(text=self.game.player.doGuess(secondWord))


def main():
    root = tk.Tk()  # Create a window
    root.title("Adventure World with GUI")  # Set window title
    root.geometry("650x450")  # Set window size
    root.resizable(False, False)  # Both x and y dimensions ...

    App(root)

    root.mainloop()


if __name__ == "__main__":
    main()
