# -*- coding: utf-8 -*-

from Game import Game
import pygame

pygame.init()
pygame.display.set_caption("Card matching game")
game = Game()

game.main_menu()