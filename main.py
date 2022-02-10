# -*- coding: utf-8 -*-

from Game import Game
import pygame

pygame.init()
pygame.display.set_caption("Card matching game")
game = Game(1200, 950)

game.main_menu()