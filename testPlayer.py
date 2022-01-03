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

    def testDoTakeSnack(self):
        self.player.currentRoom.name = "secret aisle"
        self.player.snacks = {'test1': 1, 'test2': 2, 'test3': 3}
        self.assertEqual('Your have chosen test1. Enjoy your snack!', self.player.doTakeSnack('test1'))
        self.assertTrue(self.player.snackChosen)
        self.assertEqual('You can only have one snack.', self.player.doTakeSnack('TEST'))

    def testDoTake(self):
        self.assertEqual('Not sure what you mean.', self.player.doTake('TestInvalidWord'))
        self.assertEqual('Take what?', self.player.doTake(None))
        self.assertEqual(self.player.doTakeBasket(), self.player.doTake('BASKET'))
        self.assertEqual(self.player.doTakeKey(), self.player.doTake('KEY'))
        self.player.snacks = {'TestKey': 'TestValue'}
        self.assertEqual(self.player.doTakeSnack('TestKey'), self.player.doTake('TestKey'))
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
        self.assertEqual("You need to a basket and a list to checkout!", self.player.doCheckOut())

        self.player.shoppingList = ["ONE", "TWO", "THREE"]
        self.player.basket = ["ONE", "TWO"]

        # Test if the remaining items needed is reported
        self.assertEqual("You still need to collect: \n THREE \n to checkout.", self.player.doCheckOut()) 

        # Test if bonus item has been guessed
        self.player.basket = ["ONE", "TWO", "THREE"]
        self.player.points = 100
        self.player.minutes = 7 # 7 minutes to prevent the score halving or doubling due to penalty / reward
        self.player.bonusItemGuessed = True
        self.assertEqual('CONGRATULATIONS! You have got all the items!\n Timer: 00:00\nYou score: 200\n', self.player.doCheckOut())

        # Test for each time:
        self.player.points = 100
        self.player.bonusItemGuessed = False     # Disable the bonus item
        self.player.checkoutExecuted = False

        # Fast player test (less than 3 minutes to double score)
        self.player.minutes = 2
        self.assertEqual('You have got all the items except for the bonus item!\nTimer: 00:00\nYou score: 200', self.player.doCheckOut())

        # Slow player test (over 8 minutes to halve score)
        self.player.points = 100
        self.player.minutes = 69
        self.player.checkoutExecuted = False
        self.assertEqual('You have got all the items except for the bonus item!\nTimer: 00:00\nYou score: 50', self.player.doCheckOut())
