class Npc:
    def __init__(self, name):
        self.name = name
        self.dialogue = []


    def addLine(self, text):
        self.dialogue.append(text)

    def speakDialogue(self):
        for line in self.dialogue:
            print(line)

