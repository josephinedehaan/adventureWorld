"""
    A non playable character class which provides
    a framework for setting up NPCs.
"""


class Npc:
    def __init__(self, name):
        """
            Constructor method
        :param name: text description for character
        """
        self.name = name
        self.dialogue = []


    def addLine(self, text):
        """
            Appends lines of text to a dialogue list.
        :param text: text to be appended
        :return: None
        """
        self.dialogue.append(text)


    def speakDialogue(self):
        """
            Iterates through dialogue list and prints all elements.
        :return: None
        """
        for line in self.dialogue:
            print(line)