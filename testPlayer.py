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


    def testDoGuess(self):
        self.player.basket = None
        self.assertEqual('You can\'t guess yet, get a basket first!', self.player.doGuess('Test'))
        self.player.basket = []
        self.assertEqual('You can only guess in aisle 2!', self.player.doGuess('Test'))
        self.test_RoomOne.name = 'aisle 2'
        self.assertEqual("Guess what?", self.player.doGuess(None))

        self.player.bonusItem = {'TestKey': 'TestValue'}
        self.assertEqual('That\'s not the correct item, try again', self.player.doGuess('IncorrectKey'))
        self.assertEqual('You have guessed the correct item! It has now been added to your basket',
                         self.player.doGuess('TestKey'))
        self.assertTrue(self.player.bonusItemGuessed)
        self.player.bonusItemGuessed = True
        self.assertEqual("You've already guessed the bonus item!", self.player.doGuess('Test'))

    def testGetRemainingItems(self):
        self.player.basket = ['test1', 'test2']
        self.player.shoppingList = ['test1', 'test2', 'test4']
        self.assertEqual({'test4'}, self.player.getRemainingItems())
        self.player.basket = None
        self.assertEqual(None, self.player.getRemainingItems())


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
