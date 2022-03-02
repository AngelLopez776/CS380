# -*- coding: utf-8 -*-

class Player:
    def __init__(self, playerNum, lives, teamNum):
        self.lives = lives
        self.streak = 0
        self.alive = True
        self.playerNum = playerNum
        self.teamNum = teamNum