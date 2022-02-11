# -*- coding: utf-8 -*-

import pygame
mainClock = pygame.time.Clock()


class Animations():
    def __init__(self):
        self.fps = 60
        
    def flip(self, cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, showFront):
        
        def halfFlip( cards, timeToFlip, movedX, maxSize, xDim, yDim, minBorder, xSize, ySize, window, firstHalf):
            running = True
            rect = []
            blackSurfaceArea = None
            #xDimStore = xDim
            for card in cards:
                blackSurfaceArea = card.image.convert()
                blackSurfaceArea = pygame.transform.smoothscale(surface = blackSurfaceArea, size = (xDim, yDim))  
                rect.append(blackSurfaceArea.get_rect(topleft = (minBorder + xSize * card.col + movedX, minBorder + ySize * card.row)))
            while running:
                i = 0
                mainClock.tick(self.fps)
                xDim -= timeToFlip
                movedX += timeToFlip/2
                for card in cards:
                    window.fill((0,0,0,0),rect[i])
                    surface = card.image.convert()
                    surface = pygame.transform.smoothscale(surface, (xDim, yDim))       
                    window.blit(surface, (minBorder + xSize * card.col + movedX, minBorder + ySize * card.row))  
                    i += 1
                pygame.display.update()
        
                if(firstHalf and xDim <= timeToFlip):
                    running = False
                if(not firstHalf and xDim >= maxSize):
                    running = False
            return xDim, movedX
        
        if((not cards[0].shown and showFront) or (cards[0].shown and not showFront)):
            movedX = 0
            xDimStore = xDim
            xDim, movedX = halfFlip(cards, timeToFlip, movedX, xDim, xDim, yDim, minBorder, xSize, ySize, window, True)        
            for card in cards:     
                if(showFront):    
                    card.show()
                else:
                    card.hide()
                card.update()
            halfFlip(cards, -timeToFlip, movedX, xDimStore, xDim, yDim, minBorder, xSize, ySize, window, False)
        pygame.event.clear()
