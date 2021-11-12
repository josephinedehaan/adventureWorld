"""
    Create a room described "description". Initially, it has
    no exits. 'description' is something like 'kitchen' or
    'an open court yard'
"""


class Room:
    def __init__(self, description, surroundings):
        """
            Constructor method
        :param description: text description for this room
        :param surroundings: detailed description of the surroundings
        to help player collect items.
        """
        self.description = description
        self.surroundings = surroundings
        self.exits = {}     # Dictionary

    def setExit(self, direction, neighbour):
        """
            Adds an exit for a room. The exit is stored as a dictionary
            entry of the (key, value) pair (direction, room)
        :param direction: The direction leading out of this room
        :param neighbour: The room that this direction takes you to
        :return: None
        """
        self.exits[direction] = neighbour

    def getShortDescription(self):
        """
            Fetch a short text description
        :return: text description
        """
        return f'Location: {self.description}, Possible directions: {self.getExits()} '

    def getLongDescription(self):
        """
            Fetch a longer description including available exits
        :return: text description
        """
        return f'You are {self.description}. {self.surroundings}. Possible directions: {self.getExits()} '

    def getExits(self):
        """
            Fetch all available exits as a list
        :return: list of all available exits
        """
        allExits = self.exits.keys()
        return list(allExits)

    def getExit(self, direction):
        """
            Fetch an exit in a specified direction
        :param direction: The direction that the player wishes to travel
        :return: Room object that this direction leads to, None if one does not exist
        """
        if direction in self.exits:
            return self.exits[direction]
        else:
            return None
