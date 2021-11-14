
"""
    A player class, to store all functions related to
    the player: these include the shopping basket and
    shopping list.
"""
from TextUI import TextUI


class Player:
    def __init__(self, currentRoom):
        self.textUI = TextUI()
        self.currentRoom = currentRoom
        self.basket = None
        self.shoppingList = []
        self.hasShoppingList = False

    def setShoppingList(self, shoppingList):
        self.shoppingList = set(shoppingList)

    def doReadShoppingList(self):
        if self.hasShoppingList:        # hasShoppingList becomes True when player speaks to Lisa
            print(self.shoppingList)    # to prevent player from seeing list before entering supermarket.
        else:
            print("You do not have a shopping list yet.")

    def doLookAround(self):
        """
            Allows the player to look around the aisles
            to see what items are available and who
            they can speak to.
            """
        self.textUI.printtoTextUI(self.currentRoom.getRoomDescription())

    def doGoCommand(self, secondWord):
        """
            Performs the GO command
        :param secondWord: the direction the player wishes to travel in
        :return: None
        """
        if secondWord == None:
            self.textUI.printtoTextUI("Go where?")
            return

        nextRoom = self.currentRoom.getExit(secondWord)
        if nextRoom == None:
            self.textUI.printtoTextUI("You can't go there.")
        else:
            self.currentRoom = nextRoom
            self.textUI.printtoTextUI(self.currentRoom.getRoomName())

    def doSpeak(self, secondWord):
        """
            Allows the player to speak to the store worker
            to get information and tips.
        """

        if secondWord == None:
            self.textUI.printtoTextUI("Talk to whom?")

        if self.currentRoom.npc != None and secondWord == self.currentRoom.npc.name:
            self.currentRoom.npc.speakDialogue()
            if secondWord == "LISA" and self.currentRoom.name == "lobby":
                self.hasShoppingList = True
        else:
            self.textUI.printtoTextUI(f"There is no {secondWord} here.")

    def doTake(self, secondWord):
        """
            Allows the player to take a basket and to take
            items to store in the basket
        """
        if secondWord == None:
            self.textUI.printtoTextUI("Take what?")

        if secondWord == "BASKET" and self.basket != None:
            self.textUI.printtoTextUI('You already have a basket!')
        elif secondWord == "BASKET" and self.currentRoom.name == "outside":
            self.textUI.printtoTextUI('There are no baskets here. Try going to the lobby.')
        elif secondWord == "BASKET" and self.currentRoom.name == "lobby":
            self.basket = []
            self.textUI.printtoTextUI('You now have a basket.')
        elif secondWord != "BASKET":
            if secondWord in self.shoppingList:  # checks if item is in shopping list
                if self.currentRoom.items == None:
                    self.textUI.printtoTextUI('No shopping items to collect here. Go in an aisle.')
                elif secondWord not in self.currentRoom.items:
                    self.textUI.printtoTextUI('This item is not in this aisle, try looking somewhere else.')
                elif secondWord in self.currentRoom.items:    # checks it item is in aisle
                    if secondWord in self.basket:
                        self.textUI.printtoTextUI('You already have collected this item.')
                    else:
                        self.basket.append(secondWord)
                        self.textUI.printtoTextUI(f'You have added {secondWord} to your basket.')
            else:
                self.textUI.printtoTextUI('Not sure what you mean.')


    def doCompare(self):
        if self.basket != None and self.hasShoppingList:
            self.textUI.printtoTextUI(f'You still need to collect: {self.shoppingList - set(self.basket)}')
        else:
            self.textUI.printtoTextUI('You can\'t compare yet.')



    def doSeeBasket(self):
        print(f'Your basket contains:{self.basket}')



    def compareListToBasket(self):
        pass

