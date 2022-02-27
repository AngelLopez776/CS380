# -*- coding: utf-8 -*-

class Player:
    def __init__(self, playerNum, lives):
        self.lives = lives
        self.streak = 1
        self.alive = True
        self.playerNum = playerNum