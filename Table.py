# -*- coding: utf-8 -*-

from Card import Card
import random
import time
import pygame
from Animations import Animations

class Table():
    def __init__(self, x, y, theme, lives, difficulty, fps):
        self.theme = theme
        self.lives = lives
        self.score = 0
        self.difficulty = difficulty
        self.table = [[0 for i in range(x)] for j in range(y)]
        self.selection = []
        self.animate = Animations(fps)
        self.createTable(x, y)
    
    def createTable(self, x, y):
        uniqueCards = int(x * y / 2)
        cards = []
        for c in range(uniqueCards):
            cards.append(Card(self.theme, c))
            cards.append(Card(self.theme, c))
            
        if ((x * y) % 2 == 1):
            if self.difficulty == 0:
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
            
    def checkMatch(self, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window):
        if self.selection[0].ID == self.selection[1].ID:
            self.selection.clear()
            return True
        
        elif self.selection[0].ID == "JOKER" or self.selection[1].ID == "JOKER":
            match = self.selection[1].ID if self.selection[1].ID != "JOKER" else self.selection[0].ID
            self.selection.clear()
            for r in self.table:
                for c in r:
                    if c.ID == match and not c.shown:
                        cards = []
                        cards.append(c)
                        self.animate.flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, True)
            return True
        
        else:
            
            cards = []
            cards.append(self.selection[0])
            cards.append(self.selection[1])
            self.selection.clear()
            time.sleep(1)
            self.animate.flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, False)

            return False
        
    def checkBomb(self, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window):
        for c in self.selection:
            if c.ID == "BOMB":
                time.sleep(1)
                for c in self.selection:
                    if not (c.ID == "BOMB"):
                        cards = []
                        cards.append(c)
                        self.animate.flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, False)

            
                self.lives = self.lives - 1
                self.selection.clear()
                
    def checkWin(self):
        for row in self.table:
            for c in row:
                if c.shown == False:
                    return False
        return True