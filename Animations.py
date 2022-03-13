import pygame, time
from pygame import mixer
from BoxColor import BoxColor

mainClock = pygame.time.Clock()


class Animations():
    frames = 2
    def __init__(self, fps):
        global frames
        self.fps = fps
        frames = self.fps
        self.boxColor = BoxColor()
    
    def readSettingFromFile(self, fName, sName):
        file = open(fName, 'r')
        string = None
        for line in file:
            if (line.startswith(sName)):
                string = line
                break
        string = string.replace(sName + "=", "")
        string = string.replace("\n", "")
        file.close()
        return string
    #visually flips a card; first half the card is flipped then it is switch to either being shown or hidden then the last half of the card is flipped
    def flip(self, cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, showFront):
        #half flips card so that it stops on being very thin
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
                    window.fill((self.boxColor.x, self.boxColor.y, self.boxColor.z),rect[i])
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
        
        self.volume = int(self.readSettingFromFile("SavedVariables.txt", "volume"))
        pygame.mixer.init()
        flipsound = pygame.mixer.Sound('Sounds/cardflip.mp3')
        flipsound.set_volume(self.volume/100)
        flipsound.play()
        
        xDim, movedX = halfFlip(cards, timeToFlip, movedX, xDim, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, True)        
        for card in cards:     
            if(showFront):    
                card.show()
            else:
                card.hide()
            card.update()
        halfFlip(cards, -timeToFlip, movedX, xDimStore, xDim, yDim, minBorder, xSize, ySize,toXCenter, window, False)
        pygame.event.clear()#removes any clicks that may have occured during the flipping animation
