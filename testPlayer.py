import unittest
from Room import Room
from Player import Player
from Npc import Npc


class TestPlayer(unittest.TestCase):
    def setUp(self):
        # Create dummy rooms
        self.test_RoomOne = Room("test room 1", "This is the first test room",
                                 ['r1i1', 'r1i2', 'r1i3'], {"2": "1 + 1 = ?"})

        self.test_RoomTwo = Room("test room 2", "This is the second test room",
                                 ['r2i1', 'r2i2', 'r2i3'], {"4": "2 + 2 = ?"})

        # Assign locations
        self.test_RoomOne.setExit("EAST", self.test_RoomTwo)
        self.test_RoomTwo.setExit("WEST", self.test_RoomOne)

        self.test_npc = Npc('NPC')
        self.test_npc.addLine('Testing')
        self.test_RoomTwo.setNpc(self.test_npc)

        # Init player
        self.player = Player(self.test_RoomOne)

    def tearDown(self):
        pass

    def testDoReadShoppingList(self):
        # Make sure a shopping list has been given
        self.player.hasShoppingList = False
        self.assertEqual(self.player.doReadShoppingList(), "You do not have a shopping list yet.")

        # Add a shopping list and make sure it's printed ok
        self.player.shoppingList = ["item1", "item2", "item3"]
        self.player.hasShoppingList = True
        self.assertEqual(self.player.doReadShoppingList(), ', '.join(self.player.shoppingList))

    def testDoGoCommand(self):
        self.assertEqual(self.player.doGoCommand('NORTH'), "You can't go there.")
        self.assertEqual('Location: test room 2. Possible directions: WEST ', self.player.doGoCommand('EAST'))

    def testDoSpeak(self):
        self.assertEqual(self.player.doSpeak(), 'There is no one to talk to here.')
        self.player.currentRoom = self.test_RoomTwo
        self.assertEqual(self.player.currentRoom.npc.speakDialogue(), 'Testing')

    def testDoTakeBasket(self):
        self.assertEqual('There are no baskets here. Try going to the lobby.', self.player.doTakeBasket())
        self.assertFalse(self.player.hasBasket)
        self.test_RoomOne.name = "lobby"
        self.assertEqual('You now have a basket.', self.player.doTakeBasket())
        self.assertTrue(self.player.hasBasket)
        self.assertEqual('You already have a basket!', self.player.doTakeBasket())

    def testDoTakeKey(self):
        self.assertEqual('There are no keys here', self.player.doTakeKey())
        self.test_RoomOne.name = "aisle 4"
        self.assertEqual("Key taken. Go find the locked door! \n There's a treat for you there.",
                         self.player.doTakeKey())
        self.assertTrue(self.player.hasKey)
        self.assertEqual('You already have taken the key', self.player.doTakeKey())

    def testDoTakeSecretItem(self):
        self.player.secretItemChosen = True
        self.assertEqual('You can only have one snack.', self.player.doTakeSecretItem('TEST'))

        pass
        # if not self.secretItemChosen and self.currentRoom.name == "secret aisle":
        #     self.points = self.secretItems.get(secondWord) + self.points
        #     self.secretItemChosen = True
        #     return f'Your have chosen {secondWord}. Enjoy your snack!'

        # elif self.secretItemChosen:
        #     return 'You can only have one snack.'

    def testDoTake(self):
        self.assertEqual('Not sure what you mean.', self.player.doTake('TestInvalidWord'))
        self.assertEqual('Take what?', self.player.doTake(None))
        self.assertEqual(self.player.doTakeBasket(), self.player.doTake('BASKET'))
        self.assertEqual(self.player.doTakeKey(), self.player.doTake('KEY'))
        self.player.secretItems = {'TestKey': 'TestValue'}
        self.assertEqual(self.player.doTakeSecretItem('TestKey'), self.player.doTake('TestKey'))
        self.player.hasBasket = False
        self.player.shoppingList = ['TestItem1', 'TestItem2']
        self.assertEqual('Go get a basket!', self.player.doTake('TestItem1'))
        self.player.hasBasket = True
        self.assertEqual('This item is not in this aisle, try looking somewhere else.',
                         self.player.doTake('TestItem1'))
        self.test_RoomOne.items = None
        self.assertEqual('No shopping items to collect here. Go in an aisle.',
                         self.player.doTake('TestItem1'))



        pass

        # elif secondWord != "BASKET":
        #     if secondWord in self.shoppingList and not self.hasBasket:
        #         return 'Go get a basket!'
        #     if secondWord in self.shoppingList and self.hasBasket:  # checks if item is in shopping list
        #         if self.currentRoom.items == None:  # only aisles have items
        #             return 'No shopping items to collect here. Go in an aisle.'
        #         elif secondWord not in self.currentRoom.items:  # valid 2nd word but invalid location
        #             self.points -= 2
        #             return 'This item is not in this aisle, try looking somewhere else.'

        #         elif secondWord in self.currentRoom.items:  # checks it item is in aisle
        #             if secondWord in self.basket:  # user has already taken item
        #                 return 'You already have collected this item.'

        #             else:
        #                 self.basket.append(secondWord)
        #                 self.points += 2
        #                 return 'Added to basket.'

    def testDoGuess(self):
        pass
        #
        # if self.basket == None:  # user can only guess with basket
        #     return 'You can\'t guess yet, get a basket first!'
        # elif self.currentRoom.name != 'aisle 2':
        #     return 'You can only guess in aisle 2!'
        # elif secondWord == None:  # alerts user that they need a 2nd word
        #     return "Guess what?"
        # elif self.bonusItemGuessed:  # bonus item has already been guessed
        #     return "You've already guessed the bonus item!"
        # elif secondWord == list(self.bonusItem.keys())[0] and self.basket != None:
        #     self.basket.extend(list(self.bonusItem.keys()))  # adds to basket
        #     self.bonusItemGuessed = True
        #     self.points += 10
        #     return 'You have guessed the correct item! It has now been added to your basket'
        # else:  # if user types incorrect answer
        #     return 'That\'s not the correct item, try again'

    def testGetRemainingItems(self):
        pass
        # if self.basket == None:  # ensures user has basket
        #     return None
        # else:  # executes comparison
        #     return set(self.shoppingList) - set(self.basket)

    def testDoCompare(self):
        pass
        #
        # itemsLeft = self.getRemainingItems()
        #
        # if itemsLeft is None:
        #     return 'You can\'t compare without a basket.'
        # if not self.hasShoppingList:
        #     return 'You need a basket and a shopping list to compare!'
        # elif self.hasShoppingList and itemsLeft != 0:  # displays items left to collect
        #     return f'You still need to collect: {", ".join(str(item) for item in itemsLeft)}'
        # else:
        #     return "Nothing left to collect! Go to checkout."

    def testDoSeePoints(self):
        pass
        # return f'Your score: {self.points}'

    def testDoCheckTime(self):
        pass
        # while self.basket is not None and self.startTime is not None:
        #     currentTime = time.time()
        #     showTimer = currentTime - self.startTime
        #     self.minutes = int(showTimer / 60)
        #     self.seconds = int(showTimer % 60)
        #     minutesStr = str(self.minutes).zfill(2)
        #     secondsStr = str(self.seconds).zfill(2)
        #     return f'{minutesStr}:{secondsStr}'
        # else:
        #     return '00:00'

    def testDoCheckOut(self):
        pass
        # itemsLeft = self.getRemainingItems()
        #
        # if itemsLeft == None:
        #     return 'You need to a basket and a list to checkout!'
        #
        # if len(self.getRemainingItems()) != 0:
        #     return f'You still need to collect: \n {", ".join(itemsLeft)} \n to checkout.'
        #
        # if self.checkoutExecuted == True:
        #     return 'You have already checked out. Goodbye!'
        #
        # if self.bonusItemGuessed:
        #     self.points *= 2
        #     self.shoppingList.extend(list(self.bonusItem.keys()))  # adds to shopping list for correct comparison
        #     if len(self.getRemainingItems()) == 0:  # executes comparison
        #         self.checkoutExecuted = True
        #         self.doCheckTime()
        #         if self.minutes < 3:
        #             self.points *= 2  # doubles points for fast play
        #         elif self.minutes > 8:
        #             self.points /= 2  # halves points for slow play
        #         self.doSeePoints()
        #         return 'CONGRATULATIONS! You have got all the items!\n ' \
        #                f'Timer: {self.doCheckTime()}\n' \
        #                f'You score: {self.points}\n'
        # elif not self.bonusItemGuessed:
        #     if len(self.getRemainingItems()) == 0:  # executes comparison
        #         self.checkoutExecuted = True
        #         self.doCheckTime()
        #         if self.minutes < 3:
        #             self.points *= 2  # doubles points for fast play
        #         elif self.minutes > 8:
        #             self.points /= 2  # halves points for slow play
        #         self.doSeePoints()
        #         return str('You have got all the items except for the bonus item!\n'
        #                    f'Timer: {self.doCheckTime()}\n'
        #                    f'You score: {self.points}')
        # else:  # alerts user that they have not collected all items
        #     return "You can't checkout until you have collected all the items on your shopping list!"
        #
        #
