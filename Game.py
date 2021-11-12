from Groceries import Groceries
from Player import Player
from Room import Room
from TextUI import TextUI

"""
    This class is the main class of the "Adventure World" application. 
    'Adventure World' is a very simple, text based adventure game.  Users 
    can walk around some scenery. That's all. It should really be extended 
    to make it more interesting!
    
    To play this game, create an instance of this class and call the "play"
    method.

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
        self.currentRoom = self.outside
        self.textUI = TextUI()
        self.player = Player()
        self.groceries = Groceries()


    def createRooms(self):
        """
            Sets up all room assets
        :return: None
        """
        self.outside = Room("outside",
                            "There's not much out here... Try going inside!")
        self.lobby = Room("in the lobby",
                          "There is a stack of baskets next to you and a friendly store worker, Lisa")
        self.aisleOne = Room("in aisle 1",
                             "There are mounds of colourful fruits and vegetables")
        self.aisleTwo = Room("in aisle 2",
                             "There are fridges full of fresh milk, cheese, meats and eggs")
        self.aisleThree = Room("in aisle 3",
                               "There are tins of soup and beans; packets of dry pasta, rice and pulses")
        self.aisleFour = Room("in aisle 4",
                              "There are rows upon rows of juices, sodas, mineral water and squash")
        self.aisleFive = Room("in aisle 5",
                              "There are boxes of tissues, a cornucopia of cleaning products and tools")
        self.checkout = Room("in the checkout",
                             "There is a friendly store worker at the checkout")

        self.outside.setExit("north", self.lobby)
        self.lobby.setExit("north", self.aisleOne)
        self.lobby.setExit("south", self.outside)
        self.aisleOne.setExit("east", self.aisleTwo)
        self.aisleOne.setExit("south", self.lobby)
        self.aisleTwo.setExit("east", self.aisleThree)
        self.aisleTwo.setExit("west", self.aisleOne)
        self.aisleThree.setExit("east", self.aisleFour)
        self.aisleThree.setExit("west", self.aisleTwo)
        self.aisleFour.setExit("east", self.aisleFive)
        self.aisleFour.setExit("west", self.aisleThree)
        self.aisleFive.setExit("west", self.aisleFour)
        self.aisleFive.setExit("south", self.checkout)
        self.checkout.setExit("north", self.aisleFive)
        self.checkout.setExit("south", self.outside)


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
        if self.currentRoom == self.outside:
            self.textUI.printtoTextUI("You are outside the supermarket. The entrance is up north.")
        self.textUI.printtoTextUI("")
        self.textUI.printtoTextUI(f'Your command words are: {self.showCommandWords()}')

    def showCommandWords(self):
        """
            Show a list of available commands
        :return: None
        """
        return ['help', 'go', 'quit', 'look', 'take', 'talk to']

    def processCommand(self, command):
        """
            Process a command from the TextUI
        :param command: a 2-tuple of the form (commandWord, secondWord)
        :return: True if the game has been quit, False otherwise
        """
        commandWord, secondWord = command
        if commandWord != None:
            commandWord = commandWord.upper()

        wantToQuit = False
        if commandWord == "HELP":
            self.doPrintHelp()
        elif commandWord == "GO":
            self.doGoCommand(secondWord)
        elif commandWord == "LOOK":
            self.doLookAround()
        elif commandWord == "TALK":
            self.doSpeak(secondWord)
        elif commandWord == "TAKE":
            self.doTake(secondWord)
        elif commandWord == "LIST":
            self.groceries.getShoppingList()
        elif commandWord == "BASKET":
            self.player.displayBasket()
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

    def doGoCommand(self, secondWord):
        """
            Performs the GO command
        :param secondWord: the direction the player wishes to travel in
        :return: None
        """
        if secondWord == None:
            # Missing second word ...
            self.textUI.printtoTextUI("Go where?")
            return

        nextRoom = self.currentRoom.getExit(secondWord)
        if nextRoom == None:
            self.textUI.printtoTextUI("There is no door!")
        else:
            self.currentRoom = nextRoom
            self.textUI.printtoTextUI(self.currentRoom.getShortDescription())

    def doLookAround(self):
        """
            Allows the player to look around the aisles
            to see what items are available and who
            they can speak to.
            """
        self.textUI.printtoTextUI(self.currentRoom.getLongDescription())

    def doSpeak(self, secondWord):
        """
            Allows the player to speak to the store worker
            to get information and tips.
        """

        if secondWord == None:
            self.textUI.printtoTextUI("Talk to whom?")

        if secondWord == "lisa" and self.currentRoom == self.lobby and self.groceries.shoppingList == []:
            self.textUI.printtoTextUI("Hello and welcome to Adventure World Supermarket! We have been waiting for you.")
            self.textUI.printtoTextUI("Here is your shopping list:")
            self.textUI.printtoTextUI(self.groceries.createShoppingList())
            self.textUI.printtoTextUI("Your goal is to fill your basket with as many of these items as possible.")
            self.textUI.printtoTextUI("You can check your list using the command word 'list'")
            self.textUI.printtoTextUI("To check what items you have in you basket, use the command word 'basket'")
            self.textUI.printtoTextUI("To see which items you still need to collect, use the command word 'compare'")


        else:
            self.textUI.printtoTextUI("There is no person with such name")


    def doTake(self, secondWord):
        """
            Allows the player to take a basket and to take
            items to store in the basket
        """
        if secondWord == None:
            self.textUI.printtoTextUI("Take what?")

        if secondWord == "basket" and self.player.basket != None:
            self.textUI.printtoTextUI('You already have a basket!')
        elif secondWord == "basket" and self.currentRoom != self.lobby:
            self.textUI.printtoTextUI('There are no baskets here. Try going to the lobby.')
        elif secondWord == "basket" and self.currentRoom == self.lobby:
            self.player.basket = []
            self.textUI.printtoTextUI('You now have a basket.')
        elif secondWord != "basket" and secondWord in self.groceries.shoppingList and secondWord not in self.player.basket:
            self.player.basket.append(secondWord)
        else:
            self.textUI.printtoTextUI('Not sure what you mean.')




def main():
    game = Game()
    game.play()


if __name__ == "__main__":
    main()