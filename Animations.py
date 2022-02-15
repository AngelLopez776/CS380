# -*- coding: utf-8 -*-

import pygame
import time
mainClock = pygame.time.Clock()


class Animations():
    frames = 2
    def __init__(self, fps):
        global frames
        self.fps = fps
        frames = self.fps

    def flip(self, cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, showFront):
        
        def halfFlip( cards, timeToFlip, movedX, maxSize, xDim, yDim, minBorder, xSize, ySize, window, firstHalf):
            global frames
            
            running = True
            rect = []
            blackSurfaceArea = None
            #xDimStore = xDim
            for card in cards:
                blackSurfaceArea = card.image.convert()
                blackSurfaceArea = pygame.transform.smoothscale(blackSurfaceArea, (xDim + 10, yDim))  
                rect.append(blackSurfaceArea.get_rect(topleft = (minBorder - 5 + xSize * card.col + movedX, minBorder + ySize * card.row)))
            while running:
                i = 0
                mainClock.tick(frames)
                deltaTime = 1000/frames/1000
                #print(deltaTime)
                xDim -= timeToFlip * deltaTime
                movedX += timeToFlip/2 * deltaTime
                for card in cards:
                    window.fill((0,0,0,0),rect[i])
                    surface = card.image.convert()
                    surface = pygame.transform.smoothscale(surface, (xDim, yDim))       
                    window.blit(surface, (minBorder + xSize * card.col + movedX, minBorder + ySize * card.row))  
                    i += 1
                pygame.display.update()
                if(firstHalf and xDim <= (timeToFlip * deltaTime)):
                    running = False
                if(not firstHalf and xDim >= maxSize):
                    running = False
            return xDim, movedX
        
        t0 = time.time()
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
        t1 = time.time()
        print(t1-t0)
        pygame.event.clear()#removes any clicks that may have occured during the flipping animation
