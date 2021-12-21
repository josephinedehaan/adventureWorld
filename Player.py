from TextUI import TextUI
import time


"""
    A player class, to store all functions related to
    the player: these include shopping basket and
    shopping list.
"""


class Player:
    def __init__(self, currentRoom):
        """
            Constructor method.
        :param currentRoom: the room the player is currently located in, starts outside.
        :return: None
        """
        self.textUI = TextUI()
        self.currentRoom = currentRoom
        self.basket = None
        self.shoppingList = []
        self.hasShoppingList = False
        self.bonusItem = {}
        self.bonusItemGuessed = False
        self.points = 0
        self.startTime = None
        self.hasKey = False


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
        if self.hasShoppingList:  # hasShoppingList becomes True when player speaks to Lisa
            print(', '.join(self.shoppingList))  # to prevent player from seeing list before entering supermarket.
        else:
            print("You do not have a shopping list yet.")

    def doLookAround(self):
        """
            Allows the player to look around the aisles
            to see what items are available and who
            they can speak to.
            :return: None
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
        :return:
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
        """
            Allows the player to take a basket and to take items to store in the basket.
        :return: None
        """
        if self.basket != None:  # so that user can only have one basket
            self.textUI.printtoTextUI('You already have a basket!')
            return
        elif self.currentRoom.name != "lobby":  # so that user can only take basket in lobby
            self.textUI.printtoTextUI('There are no baskets here. Try going to the lobby.')
        elif self.currentRoom.name == "lobby" and self.basket is None:  # creates basket
            self.basket = []
            self.textUI.printtoTextUI('You now have a basket.')
            self.startTime = time.time()

    def doTakeKey(self):
        """

        :return:
        """
        if self.hasKey:       # player cannot take the key more than once.
            self.textUI.printtoTextUI('You already have taken the key')
        elif self.currentRoom.name != "aisle 4":  # so that user can only take key is aisle 4
            self.textUI.printtoTextUI('There are no keys here')
        elif not self.hasKey and self.currentRoom.name == "aisle 4":
            self.textUI.printtoTextUI('Key taken. Find the locked door!')
            self.hasKey = True




    def doTake(self, secondWord):
        """
            Allows the player to take a basket and to take items to store in the basket.
        :param secondWord: name of the item player wants to take.
                Item can be a basket which creates a list, or
                a grocery item which is stored in the basket list.
        """
        if secondWord == None:
            self.textUI.printtoTextUI("Take what?")  # makes sure user typed 2nd word
        elif secondWord == "BASKET":
            self.doTakeBasket()  # if 2nd word is right user takes basket
        elif secondWord == "KEY":
            self.doTakeKey()
        elif secondWord != "BASKET":
            if secondWord in self.shoppingList:  # checks if item is in shopping list
                if self.currentRoom.items == None:  # only aisles have items
                    self.textUI.printtoTextUI('No shopping items to collect here. Go in an aisle.')
                elif secondWord not in self.currentRoom.items:  # valid 2nd word but invalid location
                    self.textUI.printtoTextUI('This item is not in this aisle, try looking somewhere else.')
                    self.points -= 1
                elif secondWord in self.currentRoom.items:  # checks it item is in aisle
                    if secondWord in self.basket:  # user has already taken item
                        self.textUI.printtoTextUI('You already have collected this item.')
                    else:
                        self.basket.append(secondWord)
                        self.textUI.printtoTextUI(f'You have added {secondWord} to your basket.')
                        self.points += 1
            else:
                self.textUI.printtoTextUI('Not sure what you mean.')

    def doGuess(self, secondWord):
        """
            Allows the player to guess the bonus item.
        :param secondWord: the name of the store worker the player wishes to speak to.
        :return:
        """
        if secondWord == list(self.bonusItem.keys())[0] and self.basket != None:
            self.textUI.printtoTextUI('You have guessed the correct item! It has now been added to your basket')
            self.basket.extend(list(self.bonusItem.keys()))  # adds to basket
            self.bonusItemGuessed = True
        elif self.basket == None:  # user can only guess with basket
            self.textUI.printtoTextUI('You can\'t guess yet, get a basket first!')
        elif secondWord == None:  # alerts user that they need a 2nd word
            self.textUI.printtoTextUI("Guess what?")
        elif self.bonusItemGuessed:  # bonus item has already been guessed
            self.textUI.printtoTextUI("You've already guessed the bonus item!")
        else:  # if user types incorrect answer
            self.textUI.printtoTextUI('That\'s not the correct item, try again')

    def getRemainingItems(self):
        """
            Checks difference between shopping list and basket
        :return: Set containing difference
        """
        if self.basket == None:  # ensures user has basket
            return None
        else:  # executes comparison
            return set(self.shoppingList) - set(self.basket)

    def doCompare(self):
        """
            Compares shopping list to current basket and prints the items
            which still need to be collected.
        :param: None
        :return itemsLeft: Set containing difference
        """
        itemsLeft = self.getRemainingItems()

        if itemsLeft == None:
            self.textUI.printtoTextUI('You can\'t compare without a basket.')
            return

        if self.hasShoppingList == False:
            self.textUI.printtoTextUI('You need a basket and a shopping list to compare!')
        elif self.hasShoppingList and itemsLeft != 0:  # displays items left to collect
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
        if self.basket is None:  # alerts user can only check basket if they have a basket
            self.textUI.printtoTextUI("You still need to take a basket.")
        elif len(self.basket) == 0:  # alerts user that basket is empty
            self.textUI.printtoTextUI("Your basket is empty. Go fill it up!")
        else:  # displays items in basket
            self.textUI.printtoTextUI(f'Your basket contains: {", ".join(self.basket)}')

    def doSeePoints(self):
        """
            Displays score.
        :param: None
        :return: None
        """
        self.textUI.printtoTextUI(f'Your score: {self.points}')

    def doCheckTime(self):
        """
            Checks timer.
        :param: None
        :return: None
        """
        currentTime = time.time()
        showTimer = currentTime - self.startTime
        minutes = int(showTimer/60)
        seconds = int(showTimer % 60)

        if self.basket is not None:
            self.textUI.printtoTextUI(f'Time: {minutes}:{seconds}')
        else:
            self.textUI.printtoTextUI('Timer starts once you have collected your basket.')

        return minutes

    def doCheckOut(self):
        """
            Allows the player to checkout and complete the game.
        :return: None
        """
        itemsLeft = self.getRemainingItems()

        if itemsLeft == None:
            return

        if self.bonusItemGuessed:
            self.points *= 2
            self.shoppingList.extend(list(self.bonusItem.keys()))  # adds to shopping list for correct comparison
            if len(self.getRemainingItems()) == 0:  # executes comparison
                self.textUI.printtoTextUI('CONGRATULATIONS! You have got all the items!')
                self.doCheckTime()
                if self.doCheckTime() < 3:
                    self.points *= 2    # doubles points for fast play
                elif self.doCheckTime() > 8:
                    self.points /= 2    # halves points for slow play
                self.doSeePoints()
                exit()
        elif not self.bonusItemGuessed:
            if len(self.getRemainingItems()) == 0:  # executes comparison
                self.textUI.printtoTextUI('You have got all the items except for the bonus item!')
                self.doCheckTime()
                if self.doCheckTime() < 3:
                    self.points *= 2    # doubles points for fast play
                elif self.doCheckTime() > 8:
                    self.points /= 2    # halves points for slow play
                self.doSeePoints()
                exit()
        else:  # alerts user that they have not collected all items
            self.textUI.printtoTextUI(
                "You can't checkout until you have collected all the items on your shopping list!")