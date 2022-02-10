# -*- coding: utf-8 -*-

import pygame

class Animations():
    def __init__(self, clock):
        self.fps = 60
        self.mainClock = clock
        
    def flip(self, cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, front):
        movedX = 0
        xDimStore = xDim
        xDim, movedX = self.halfFlip(cards, timeToFlip, movedX, xDim, xDim, yDim, minBorder, xSize, ySize, window, True)        
        for card in cards:     
            if(front):    
                card.show()
            else:
                card.hide()
            card.update()
        
        self.halfFlip(cards, -timeToFlip, movedX, xDimStore, xDim, yDim, minBorder, xSize, ySize, window, False)
            
    def halfFlip(self, cards, timeToFlip, movedX, maxSize, xDim, yDim, minBorder, xSize, ySize, window, firstHalf):
        running = True
        rect = []
        blackSurfaceArea = None
        #xDimStore = xDim
        for card in cards:
            blackSurfaceAreaO = card.image.convert()
            blackSurfaceArea = pygame.transform.smoothscale(blackSurfaceAreaO, (xDim, yDim))  
            rect.append(blackSurfaceArea.get_rect(topleft = (minBorder + xSize * card.col + movedX, minBorder + ySize * card.row)))
        while running:
            i = 0
            self.mainClock.tick(self.fps)
            xDim -= timeToFlip
            movedX += timeToFlip/2
            for card in cards:
                window.fill((0, 0, 0),rect[i])
                surface =  card.image.convert()
                surface = pygame.transform.smoothscale(surface, (xDim, yDim))       
                window.blit(surface, (minBorder + xSize * card.col + movedX, minBorder + ySize * card.row))  
                i += 1
            pygame.display.update()
    
            if(firstHalf and xDim <= timeToFlip):
                running = False
            if(not firstHalf and xDim >= maxSize):
                running = False
        return xDim, movedX