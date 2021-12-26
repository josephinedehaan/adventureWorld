"""
    A room class which provides a framework
    for setting up all room assets.
"""


class Room:
    def __init__(self, name, description, items, bonusItem):
        """
            Constructor method.
        :param name: text description for this room.
        :param description: detailed description of the surroundings
                            to help player collect items.
        :param items: items stored in this room (if any).
        :param bonusItems: bonus 'secret' items stored in this room (if any).
        """
        self.bonusItem = bonusItem
        self.items = items
        self.name = name
        self.description = description
        self.exits = {}
        self.npc = None

    def setNpc(self, npc):
        """
            Assigns non playable characters to selected rooms.
        :param npc: The name of the non playable character.
        :return: None
        """
        self.npc = npc

    def setExit(self, direction, neighbour):
        """
            Adds an exit for a room. The exit is stored as a dictionary
            entry of the (key, value) pair (direction, room).
        :param direction: The direction leading out of this room.
        :param neighbour: The room that this direction takes you to.
        :return: None
        """
        self.exits[direction] = neighbour

    def getRoomName(self):

        return self.name

    def getRmNameAndExits(self):
        """
            Fetch name and exits of room.
        :return: text description.
        """
        return f'Location: {self.name}, Possible directions: {self.getExits()} '

    def getRoomDescription(self):
        """
            Fetch a  description including available exits
        :return: text description.
        """
        return f'{self.description}. Possible directions: {self.getExits()} '

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
