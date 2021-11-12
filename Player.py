"""
    A player class, to store all functions related to
    the player: these include the shopping basket and
    shopping list.
"""


class Player:
    def __init__(self):
        self.basket = None

    def displayBasket(self):
        print(f'Your basket contains:{self.basket}')

    def displayShoppingList(self):
        pass

    def compareListToBasket(self):
        pass

