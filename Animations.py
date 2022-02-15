# -*- coding: utf-8 -*-

import pygame
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
            deltaTime = 1000/frames/1000
            running = True
            rect = []
            blackSurfaceArea = None
            #xDimStore = xDim
            for card in cards:
                blackSurfaceArea = card.image.convert()
                blackSurfaceArea = pygame.transform.smoothscale(blackSurfaceArea, (int(xDim), int(yDim)))  
                rect.append(blackSurfaceArea.get_rect(topleft = (minBorder + xSize * card.col + movedX, minBorder + ySize * card.row)))
            while running:
                i = 0
                mainClock.tick(frames)
                #print(deltaTime)
                xDim -= timeToFlip * deltaTime
                movedX += timeToFlip/2 * deltaTime
                for card in cards:
                    window.fill((0,0,0,0),rect[i])
                    surface = card.image.convert()
                    surface = pygame.transform.smoothscale(surface, (int(xDim), int(yDim)))       
                    window.blit(surface, (minBorder + xSize * card.col + movedX, minBorder + ySize * card.row))  
                    i += 1
                pygame.display.update()
                if(firstHalf and xDim <= (timeToFlip * deltaTime)):
                    running = False
                if(not firstHalf and xDim >= maxSize):
                    running = False
            return xDim, movedX
        
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
        pygame.event.clear()#removes any clicks that may have occured during the flipping animation
