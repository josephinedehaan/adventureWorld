import time
from Utils import gameLog

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
        self.currentRoom = currentRoom
        self.basket = None
        self.shoppingList = []
        self.hasShoppingList = False
        self.bonusItem = {}
        self.bonusItemGuessed = False
        self.points = 0
        self.startTime = None
        self.hasKey = False
        self.secretItems = {}
        self.secretItemChosen = False
        self.minutes = 0
        self.seconds = 0
        self.hasBasket = False
        self.checkoutExecuted = False

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

    def setSecretIems(self, secretItems):
        """
            Retrieves secret items from Game.
        :param bonusItem:
        :return: None
        """
        self.secretItems = secretItems

    def doReadShoppingList(self):
        """
            Prints shopping list if the player has collected it.
        :param: None
        :return: None

        """
        if self.hasShoppingList:  # hasShoppingList becomes True when player speaks to Lisa
            return ', '.join(self.shoppingList)  # to prevent player from seeing list before entering supermarket.
        else:
            return "You do not have a shopping list yet."

    def doGoCommand(self, secondWord):
        """
            Performs the GO command
        :param secondWord: the direction the player wishes to travel in
        :return: None
        """
        nextRoom = self.currentRoom.getExit(secondWord)

        if nextRoom == None:
            return "You can't go there."
        else:
            self.currentRoom = nextRoom
            gameLog(f'User went: {secondWord}')
            return self.currentRoom.getRmNameAndExits()

    def doSpeak(self):
        """
            Allows the player to speak to the store workers
            to get information and tips.
        :return:
        """

        if self.currentRoom.npc != None:
            gameLog(f'User spoke to: {self.currentRoom.npc.name}')
            if self.currentRoom.name == "lobby":
                self.hasShoppingList = True
                return self.currentRoom.npc.speakDialogue()
            if self.currentRoom.name == "aisle 2":
                return self.currentRoom.npc.speakDialogue() + list(self.bonusItem.values())[0]
            if self.currentRoom.name == "secret aisle":
                return self.currentRoom.npc.speakDialogue()
            if self.currentRoom.name == "checkout":
                return self.currentRoom.npc.speakDialogue() + self.doCheckOut()
        else:
            return f"There is no one to talk to here."

    def doTakeBasket(self):
        """
            Allows the player to take a basket and to take items to store in the basket.
        :return: None
        """
        if self.basket != None:  # so that user can only have one basket
            return 'You already have a basket!'
        elif self.currentRoom.name != "lobby":  # so that user can only take basket in lobby
            return 'There are no baskets here. Try going to the lobby.'
        elif self.currentRoom.name == "lobby" and self.basket is None:  # creates basket
            gameLog('User took: BASKET')
            self.basket = []
            self.startTime = time.time()
            self.hasBasket = True
            return 'You now have a basket.'

    def doTakeKey(self):
        """
                TO DO
        :return:
        """
        if self.hasKey:  # player cannot take the key more than once.
            return 'You already have taken the key'
        elif self.currentRoom.name != "aisle 4":  # so that user can only take key is aisle 4
            return 'There are no keys here'
        elif not self.hasKey and self.currentRoom.name == "aisle 4":
            self.hasKey = True
            gameLog('User took: KEY')
            return "Key taken. Go find the locked door! \n There's a treat for you there."

    def doTakeSecretItem(self, secondWord):
        """
                TO DO
        :return:
        """
        if not self.secretItemChosen and self.currentRoom.name == "secret aisle":
            self.points = self.secretItems.get(secondWord) + self.points
            self.secretItemChosen = True
            gameLog(f'User took snack: {secondWord}')
            return f'Your have chosen {secondWord}. Enjoy your snack!'
        elif self.secretItemChosen:
            gameLog('User tried taking snack twice.')
            return 'You can only have one snack.'

    def doTake(self, secondWord):
        """
            Allows the player to take a basket and to take items to store in the basket.
        :param secondWord: name of the item player wants to take.
                Item can be a basket which creates a list, or
                a grocery item which is stored in the basket list.
        """
        if secondWord == None:
            gameLog('User did not input second command word.')
            return "Take what?"  # makes sure user typed 2nd word
        elif secondWord == "BASKET":
            return self.doTakeBasket()  # if 2nd word is right user takes basket
        elif secondWord == "KEY":
            return self.doTakeKey()
        elif secondWord in self.secretItems.keys():
            return self.doTakeSecretItem(secondWord)
        elif secondWord != "BASKET":
            if secondWord in self.shoppingList and not self.hasBasket:
                gameLog('User tried taking item without having take basket.')
                return 'Go get a basket!'
            if secondWord in self.shoppingList and self.hasBasket:  # checks if item is in shopping list
                if self.currentRoom.items == None:  # only aisles have items
                    gameLog('User tried taking item in a room without items.')
                    return 'No shopping items to collect here. Go in an aisle.'
                elif secondWord not in self.currentRoom.items:  # valid 2nd word but invalid location
                    self.points -= 2
                    gameLog(f'User tried taking {secondWord} in the wrong aisle')
                    return 'This item is not in this aisle, try looking somewhere else.'
                elif secondWord in self.currentRoom.items:  # checks it item is in aisle
                    if secondWord in self.basket:  # user has already taken item
                        gameLog(f'User tried taking {secondWord} again.')
                        return 'You already have collected this item.'
                    else:
                        gameLog(f'User took: {secondWord}')
                        self.basket.append(secondWord)
                        self.points += 2
                        return 'Added to basket.'
            else:
                return 'Not sure what you mean.'

    def doGuess(self, secondWord):
        """
            Allows the player to guess the bonus item.
        :param secondWord: the name of the store worker the player wishes to speak to.
        :return:
        """

        if self.basket == None:  # user can only guess with basket
            gameLog('User tried guessing without a basket')
            return 'You can\'t guess yet, get a basket first!'
        elif self.currentRoom.name != 'aisle 2':
            gameLog('User tried guessing in the wrong aisle')
            return 'You can only guess in aisle 2!'
        elif secondWord == None:  # alerts user that they need a 2nd word
            return "Guess what?"
        elif self.bonusItemGuessed:  # bonus item has already been guessed
            gameLog('User tried guessing item after having already guessed it correctly.')
            return "You've already guessed the bonus item!"
        elif secondWord == list(self.bonusItem.keys())[0] and self.basket != None:
            self.basket.extend(list(self.bonusItem.keys()))  # adds to basket
            self.bonusItemGuessed = True
            self.points += 10
            gameLog(f'User guessed: {secondWord}')
            return 'You have guessed the correct item! It has now been added to your basket'
        else:  # if user types incorrect answer
            gameLog('User guessed incorrectly.')
            return 'That\'s not the correct item, try again'

    def getRemainingItems(self):
        """
            Checks difference between shopping list and basket
        :return: Set containing difference
        """

        if self.basket == None:  # ensures user has basket
            return None
        else:  # executes comparison
            return set(self.shoppingList) - set(self.basket)

    def doSeePoints(self):
        """
            Displays score.
        :param: None
        :return: None
        """
        return f'Your score: {self.points}'

    def doCheckTime(self):
        """
            Checks timer.
        :param: None
        :return: None
        """
        while self.basket is not None and self.startTime is not None:
            currentTime = time.time()
            showTimer = currentTime - self.startTime
            self.minutes = int(showTimer / 60)
            self.seconds = int(showTimer % 60)
            minutesStr = str(self.minutes).zfill(2)
            secondsStr = str(self.seconds).zfill(2)
            return f'{minutesStr}:{secondsStr}'
        else:
            return '00:00'

    def doCheckOut(self):
        """
            Allows the player to checkout and complete the game.
        :return: None
        """
        itemsLeft = self.getRemainingItems()

        if itemsLeft == None:
            gameLog('User tried checking out without basket and list.')
            return 'You need to a basket and a list to checkout!'

        if len(self.getRemainingItems()) != 0:
            gameLog('User tried checking out without having collected all items.')
            return f'You still need to collect: \n {", ".join(itemsLeft)} \n to checkout.'

        if self.checkoutExecuted == True:
            gameLog('User tried checking out after already checking out.')
            return 'You have already checked out. Goodbye!'

        if self.bonusItemGuessed:
            self.points *= 2
            self.shoppingList.extend(list(self.bonusItem.keys()))  # adds to shopping list for correct comparison
            if len(self.getRemainingItems()) == 0:  # executes comparison
                self.checkoutExecuted = True
                self.doCheckTime()
                if self.minutes < 3:
                    self.points *= 2  # doubles points for fast play
                elif self.minutes > 8:
                    self.points /= 2  # halves points for slow play
                self.doSeePoints()
                gameLog('User checked out successfully.')
                return 'CONGRATULATIONS! You have got all the items!\n ' \
                       f'Timer: {self.doCheckTime()}\n' \
                       f'You score: {self.points}\n'
        elif not self.bonusItemGuessed:
            if len(self.getRemainingItems()) == 0:  # executes comparison
                self.checkoutExecuted = True
                self.doCheckTime()
                if self.minutes < 3:
                    self.points *= 2  # doubles points for fast play
                elif self.minutes > 8:
                    self.points /= 2  # halves points for slow play
                self.doSeePoints()
                gameLog('User checked out successfully.')
                return str('You have got all the items except for the bonus item!\n'
                           f'Timer: {self.doCheckTime()}\n'
                           f'You score: {self.points}')
        # else:  # alerts user that they have not collected all items
        #     return "You can't checkout until you have collected all the items on your shopping list!"
