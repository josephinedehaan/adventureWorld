import random

class Groceries:
    def __init__(self):
        self.inventory = [['Apples', 'Bananas', 'Celery', 'Carrots', 'Melon', 'Grapes', 'Broccoli', 'Avocados'],
                          ['Eggs', 'Yoghurt', 'Milk', 'Cheddar', 'Feta', 'Chicken', 'Fishcakes', 'Ham'],
                          ['Rice', 'Pasta', 'Spaghetti', 'Lentils', 'Beans', 'Soup', 'Crackers'],
                          ['Red Wine', 'Lemonade', 'Orange Juice', 'Sparkling Water', 'Squash'],
                          ['Toilet Roll', 'Kitchen Roll', 'Tissues', 'Bleach', 'Sponges', 'Baby Wipes']]
        self.shoppingList = []


    def createShoppingList(self):
        index = 0
        while index < 5:
            self.shoppingList.extend(random.sample(self.inventory[index], 2))
            index += 1

        return ', '.join(self.shoppingList)


    def getShoppingList(self):
        print(', '.join(self.shoppingList))





