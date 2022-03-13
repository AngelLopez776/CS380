from Card import Card
import random

class Table():
    def __init__(self, x, y, theme, lives, difficulty,fps):
        self.x = x
        self.y = y
        self.theme = theme
        self.lives = lives
        self.score = 0
        self.difficulty = difficulty
        self.table = [[0 for i in range(x)] for j in range(y)]
        self.selection = []
        self.createTable(x, y)
    
    def createTable(self, x, y):
        uniqueCards = int(x * y / 2)
        cards = []
        for c in range(uniqueCards):
            cards.append(Card(self.theme, c))
            cards.append(Card(self.theme, c))
            
        if ((x * y) % 2 == 1):
            if self.difficulty == 1:
                cards.append(Card(self.theme, "JOKER"))
            else:
                cards.append(Card(self.theme, "BOMB"))
        
        random.shuffle(cards)
        count = 0
        for i in range(y):
            for j in range(x):
                self.table[i][j] = cards[count]
                count = count + 1
                
    def showAll(self):
        for r in self.table:
            for c in r:
                c.show()
                c.update()
        
    def hideAll(self):
       for r in self.table:
            for c in r:
                c.hide()
                c.update()
                
    def update(self):
        for r in self.table:
            for c in r:
                c.update()
            
    def checkMatch(self):
        if self.selection[0].ID == self.selection[1].ID:
            return 0
        
        elif self.selection[0].ID == "JOKER" or self.selection[1].ID == "JOKER":
            return 1
        
        else:       
            return 2
        
    def checkBomb(self):
        for c in self.selection:
            if c.ID == "BOMB":
                return True
                
                
    def checkWin(self):
        for row in self.table:
            for c in row:
                if c.shown == False:
                    if c.ID == "BOMB" or c.ID == "JOKER":
                        continue
                    else:
                        return False
        
        return True