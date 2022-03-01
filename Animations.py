# -*- coding: utf-8 -*-

import pygame
from pygame import mixer
import time

mainClock = pygame.time.Clock()


class Animations():
    frames = 2
    def __init__(self, fps):
        global frames
        self.fps = fps
        frames = self.fps

    def flip(self, cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, showFront):
        def halfFlip(cards, timeToFlip, movedX, maxSize, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, firstHalf):
            global frames
            deltaTime = 1000/frames/1000
            running = True
            rect = []
            blackSurfaceArea = None
            for card in cards:
                blackSurfaceArea = card.image.convert()
                blackSurfaceArea = pygame.transform.smoothscale(blackSurfaceArea, (int(xDim), int(yDim)))  
                rect.append(blackSurfaceArea.get_rect(topleft = ((minBorder + toXCenter) + xSize * card.col + movedX, minBorder + ySize * card.row)))
            while running:
                i = 0
                mainClock.tick(frames)
                xDim -= timeToFlip * deltaTime
                movedX += timeToFlip/2 * deltaTime
                for card in cards:
                    window.fill((0,0,0,0),rect[i])
                    surface = card.image.convert()
                    surface = pygame.transform.smoothscale(surface, (int(xDim), int(yDim)))       
                    window.blit(surface, ((minBorder + toXCenter) + xSize * card.col + movedX, minBorder + ySize * card.row))  
                    i += 1
                pygame.display.update()
                if(firstHalf and xDim <= (timeToFlip * deltaTime)):
                    running = False
                if(not firstHalf and xDim >= maxSize):
                    running = False
            return xDim, movedX
        
        movedX = 0
        xDimStore = xDim
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('Sounds/cardflip.mp3'))
        xDim, movedX = halfFlip(cards, timeToFlip, movedX, xDim, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, True)        
        for card in cards:     
            if(showFront):    
                card.show()
            else:
                card.hide()
            card.update()
        halfFlip(cards, -timeToFlip, movedX, xDimStore, xDim, yDim, minBorder, xSize, ySize,toXCenter, window, False)
        pygame.event.clear()#removes any clicks that may have occured during the flipping animation
