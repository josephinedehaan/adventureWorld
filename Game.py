from Player import Player
from Room import Room
from TextUI import TextUI

import random

"""
    This class is the main class of the "Adventure World" application. 

    This main class creates and initialises all the others: it creates all
    rooms, creates the parser and starts the game.  It also evaluates and
    executes the commands that the parser returns.
    
    This game is adapted from the 'World of Zuul' by Michael Kolling
    and David J. Barnes. The original was written in Java and has been
    simplified and converted to Python by Kingsley Sage
"""
class Game:

    def __init__(self):
        """
        Initialises the game
        """
        self.createRooms()
        self.textUI = TextUI()
        self.player = Player(self.outside)
        # player.setShoppingList(shoppingList) # This now gives that shopping list to the player. The
        # player has a self.ShoppingList which the passed in variable gets set to via this function.
        # the player will technically have the shopping list before they collect it. but u can do a
        # boolean in player class like 'hasShoppingList' which prevents them from using it before they
        # tke it from lisa.
        self.tempShoppingList = []
        self.createShoppingList()
        self.player.setShoppingList(self.tempShoppingList)
        self.inAisle = False


    def createRooms(self):
        """
            Sets up all room assets
        :return: None
        """

        self.outside = Room("outside", "There's not much out here... Try going inside!", None)

        self.lobby = Room("lobby", "There is a stack of baskets next to you and a friendly store worker, Lisa",
                          None)

        self.aisleOne = Room("aisle 1", "There are mounds of colourful fruits and vegetables",
                             ['APPLES', 'BANANAS', 'CELERY', 'CARROTS', 'MELON', 'GRAPES', 'BROCCOLI', 'AVOCADOS'])

        self.aisleTwo = Room("aisle 2", "There are fridges full of fresh milk, cheese, meats and eggs",
                             ['EGGS', 'YOGHURT', 'MILK', 'CHEDDAR', 'FETA', 'CHICKEN', 'FISHCAKES', 'HAM'])

        self.aisleThree = Room("aisle 3", "There are tins of soup and beans; packets of dry pasta, rice and pulses",
                               ['RICE', 'PASTA', 'SPAGHETTI', 'LENTILS', 'BEANS', 'SOUP', 'CRACKERS'])

        self.aisleFour = Room("aisle 4", "There are rows upon rows of juices, sodas, mineral water and squash",
                              ['RED WINE', 'LEMONADE', 'JUICE', 'WATER', 'COCA COLA', 'ICED TEA'])

        self.aisleFive = Room("aisle 5", "There are boxes of tissues, a cornucopia of cleaning products and tools",
                              ['TOILET ROLL', 'KITCHEN ROLL', 'TISSUES', 'BLEACH', 'SPONGES', 'BABY WIPES'])

        self.checkout = Room("checkout", "There is a friendly store worker at the checkout", None)

        self.aisles = [self.aisleOne, self.aisleTwo, self.aisleThree, self.aisleFour, self.aisleFive]


        self.outside.setExit("NORTH", self.lobby)
        self.lobby.setExit("NORTH", self.aisleOne)
        self.lobby.setExit("SOUTH", self.outside)
        self.aisleOne.setExit("EAST", self.aisleTwo)
        self.aisleOne.setExit("SOUTH", self.lobby)
        self.aisleTwo.setExit("EAST", self.aisleThree)
        self.aisleTwo.setExit("WEST", self.aisleOne)
        self.aisleThree.setExit("EAST", self.aisleFour)
        self.aisleThree.setExit("WEST", self.aisleTwo)
        self.aisleFour.setExit("EAST", self.aisleFive)
        self.aisleFour.setExit("WEST", self.aisleThree)
        self.aisleFive.setExit("WEST", self.aisleFour)
        self.aisleFive.setExit("SOUTH", self.checkout)
        self.checkout.setExit("NORTH", self.aisleFive)
        self.checkout.setExit("SOUTH", self.outside)

    def createShoppingList(self):
        for aisle in self.aisles:
            self.tempShoppingList.extend(random.sample(aisle.items, 2))

        return self.tempShoppingList

    def play(self):
        """
            The main play loop
        :return: None
        """
        self.printWelcome()
        finished = False
        while (finished == False):
            command = self.textUI.getCommand()      # Returns a 2-tuple
            finished = self.processCommand(command)

        print("Thank you for playing!")

    def printWelcome(self):
        """
            Displays a welcome message
        :return:
        """
        self.textUI.printtoTextUI("Welcome to Adventure World Supermarket!")
        self.textUI.printtoTextUI(f'Your command words are: {self.showCommandWords()}')
        self.textUI.printtoTextUI("")
        if self.player.currentRoom == self.outside:
            self.textUI.printtoTextUI("You are outside the supermarket. The entrance is up north.")

    def showCommandWords(self):
        """
            Show a list of available commands
        :return: None
        """
        return ['help', 'go', 'quit', 'look', 'take', 'talk to', 'list', 'basket', 'compare']



    def processCommand(self, command):
        """
            Process a command from the TextUI
        :param command: a 2-tuple of the form (commandWord, secondWord)
        :return: True if the game has been quit, False otherwise
        """
        commandWord, secondWord = command
        if commandWord != None:
            commandWord = commandWord.upper()
        if secondWord != None:
            secondWord = secondWord.upper()

        wantToQuit = False
        if commandWord == "HELP":
            self.doPrintHelp()
        elif commandWord == "GO":
            self.player.doGoCommand(secondWord)
        elif commandWord == "LOOK":
            self.player.doLookAround()
        elif commandWord == "TALK":
            self.player.doSpeak(secondWord)
        elif commandWord == "TAKE":
            self.player.doTake(secondWord)
        elif commandWord == "LIST":
            self.player.doReadShoppingList()
        elif commandWord == "BASKET":
            self.player.doSeeBasket()
        elif commandWord == "QUIT":
            wantToQuit = True
        else:
            # Unknown command ...
            self.textUI.printtoTextUI("Don't know what you mean")

        return wantToQuit

    def doPrintHelp(self):
        """
            Display some useful help text
        :return: None
        """
        self.textUI.printtoTextUI("Welcome to Adventure World Supermarket!")
        self.textUI.printtoTextUI("You are outside the supermarket. The entrance is up north.")
        self.textUI.printtoTextUI("")
        self.textUI.printtoTextUI(f'Your command words are: {self.showCommandWords()}')


def main():
    game = Game()
    game.play()

if __name__ == "__main__":
    main()