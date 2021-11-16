from TextUI import TextUI

"""
    A player class, to store all functions related to
    the player: these include shopping basket and
    shopping list.
"""

class Player:
    """
        Constructor method.
    :param currentRoom: the room the player is currently
                        located in, starts outside.
    :return: None
    """
    def __init__(self, currentRoom):
        self.textUI = TextUI()
        self.currentRoom = currentRoom
        self.basket = None
        self.shoppingList = []
        self.hasShoppingList = False
        self.bonusItem = {}
        self.bonusItemGuessed = False

    def setShoppingList(self, shoppingList):
        """
            Retrieves shopping list from Game and
            converts shopping list to a set.
        :param shoppingList:
        :return: None
        """
        self.shoppingList = shoppingList

    def setBonusItem(self, bonusItem):
        """
            Retrieves bonus item from Game.
        :param bonusItem:
        :return: None
        """
        self.bonusItem = bonusItem

    def doReadShoppingList(self):
        """
            Prints shopping list if the player has collected it.
        :param: None
        :return: None
        """
        if self.hasShoppingList:        # hasShoppingList becomes True when player speaks to Lisa
            print(', '.join(self.shoppingList))    # to prevent player from seeing list before entering supermarket.
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
            Allows the player to speak to the store workers
            to get information and tips.
        :param secondWord: the name of the store worker the player wishes to speak to.
        """

        if secondWord == None:
            self.textUI.printtoTextUI("Talk to whom?")

        if self.currentRoom.npc != None and secondWord == self.currentRoom.npc.name:
            self.currentRoom.npc.speakDialogue()
            if secondWord == "LISA" and self.currentRoom.name == "lobby":
                self.hasShoppingList = True
            if secondWord == "SAM" and self.currentRoom.name == "aisle 2":
                print(list(self.bonusItem.values())[0])
            if secondWord == "DOT" and self.currentRoom.name == "checkout":
                self.doCheckOut()
        elif secondWord != None:
            self.textUI.printtoTextUI(f"There is no one called {secondWord} here.")

    def doTakeBasket(self):
        if self.basket != None:
            self.textUI.printtoTextUI('You already have a basket!')
            return
        elif self.currentRoom.name != "lobby":
            self.textUI.printtoTextUI('There are no baskets here. Try going to the lobby.')
        elif self.currentRoom.name == "lobby" and self.basket == None:
            self.basket = []
            self.textUI.printtoTextUI('You now have a basket.')

    def doTake(self, secondWord):
        """
            Allows the player to take a basket and to take
            items to store in the basket.
        :param secondWord: name of the item player wants to take.
                Item can be a basket which creates a list, or
                a grocery item which is stored in the basket list.
        """
        if secondWord == None:
            self.textUI.printtoTextUI("Take what?")
        elif secondWord == "BASKET":
            self.doTakeBasket()
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


    def doGuess(self, secondWord):
        if secondWord == list(self.bonusItem.keys())[0] and self.basket != None:
            self.textUI.printtoTextUI('You have guessed the correct item! It has now been added to your basket')
            self.basket.extend(list(self.bonusItem.keys()))         # adds to basket
            self.bonusItemGuessed = True
        elif self.basket == None:
            self.textUI.printtoTextUI('You can\'t guess yet, get a basket first!')
        elif secondWord == None:
            self.textUI.printtoTextUI("Guess what?")
        elif self.bonusItemGuessed:
            self.textUI.printtoTextUI("You've already guessed the bonus item!")
        else:
            self.textUI.printtoTextUI('That\'s not the correct item, try again')

    def getRemaningItems(self):
        if self.basket == None:
            return None
        else:
            return set(self.shoppingList) - set(self.basket)

    def doCompare(self):
        """
            Compares shopping list to current basket and prints the items
            which still need to be collected.
        :param: None
        :return: None
        """
        itemsLeft = self.getRemaningItems()
        if itemsLeft == None:
            self.textUI.printtoTextUI('You can\'t compare without a basket.')
            return


        if self.hasShoppingList == False:
            self.textUI.printtoTextUI('You need a basket and a shopping list to compare!')
        elif self.hasShoppingList and itemsLeft != 0:
            self.textUI.printtoTextUI(f'You still need to collect: {", ".join(str(item) for item in itemsLeft)}')
        else:
            self.textUI.printtoTextUI("Nothing left to collect! Go to checkout.")



        return itemsLeft

    def doSeeBasket(self):
        """
            Displays the contents of the basket.
        :param: None
        :return: None
        """
        if self.basket is None:
            self.textUI.printtoTextUI("You still need to take a basket.")
        elif len(self.basket) == 0:
            self.textUI.printtoTextUI("Your basket is empty. Go fill it up!")
        else:
            print(f'Your basket contains: {", ".join(self.basket)}')

    def doCheckOut(self):
        itemsLeft = self.getRemaningItems()

        if itemsLeft == None:
            return

        if self.bonusItemGuessed:
            self.shoppingList.extend(list(self.bonusItem.keys()))   # adds to shopping list for
            if len(self.getRemaningItems()) == 0:                                 # comparison
                print('CONGRATULATIONS! You have got all the items!')
                exit()
        elif not self.bonusItemGuessed:
            if len(self.getRemaningItems()) == 0:
                print('You have got all the items except for the bonus item!')
                exit()
        else:
            print("You can't checkout until you have collected all the items on your shopping list!")

