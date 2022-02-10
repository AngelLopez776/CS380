import pygame, sys
import random
import time

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
screenWidth = 1200
screenHeight = 950
screen = pygame.display.set_mode((screenWidth, screenHeight),0,32)

font = pygame.font.SysFont(None, 20)
lifeFont = pygame.font.SysFont('Times New Roman', 20)
endFont = pygame.font.SysFont('Times New Roman', 32)

green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)


class Card():
    def __init__(self, theme, ID):
        super().__init__()

        self.ID = ID
        self.col = 0
        self.row = 0

        folder = "theme_" + str(theme) + "/"
        img = str(ID) + ".jpg"

        path = (folder + img)
        try:
            self.front_image = pygame.image.load(path)
        except FileNotFoundError:
            self.front_image = pygame.image.load(folder + "default.jpg") 
            
        self.back_image = pygame.image.load(folder + "card_back.jpg")
    
        self.image = self.back_image
        self.rect = self.image.get_rect()
        self.shown = False

    def update(self):
        if self.shown: 
            self.image = self.front_image
        else:
            self.image = self.back_image
    
    # Boolean for showing up or not
    def show(self):
        self.shown = True
    
    def hide(self):
        self.shown = False

    def makeRect(self, x, y):
        self.rect.topleft = (x, y)
    
class Table():
    def __init__(self, x, y, theme, lives):
        self.theme = theme
        self.lives = lives
        self.x = x
        self.y = y
        self.table = [[0 for i in range(x)] for j in range(y)]
        self.selection = []
        self.createTable() 
      
    #Creates the randomized table of pairs, used internally when the table is made
    def createTable(self):
        uniqueCards = int(self.x * self.y / 2)
        cards = []
        for c in range(uniqueCards):
            cards.append(Card(self.theme, c))
            cards.append(Card(self.theme, c))
            
        random.shuffle(cards)
        count = 0
        for i in range(self.y):
            for j in range(self.x):
                self.table[i][j] = cards[count]
                count = count + 1

    #Shows all cards, waits five seconds, hides all cards
    def showAll(self):
        for r in self.table:
            for c in r:
                c.show()
                c.update()
        
    def hideAll(self):
        for r in self.table:
            for c in r:
                c.hide()
                c.update()

    def update(self):
        for r in self.table:
            for c in r:
                c.update()
                
    def checkMatch(self, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, fps):
        if self.selection[0].ID == self.selection[1].ID:
            self.selection.clear()
            return True
        else:
            time.sleep(1)
            #self.selection[0].hide()
            #self.selection[1].hide()
            flip(self.selection, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, fps, False)
            #flip(self.selection[0], timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, fps, False)
            self.selection.clear()
            return False


    def drawBoard(self, window, cols, rows, xDim, yDim, minBorder, xSize, ySize):
        self.update()
        for i in range(cols):
            for j in range(rows):
                window.blit(self.table[j][i].image, (25 + (140 * i), 25 + (190 * j)))
                self.table[j][i].makeRect(25 + (140 * i), 25 + (190 * j))
        pygame.display.update()
        
        for i in range(cols):
                for j in range(rows):
                    surface = self.table[j][i].image.convert()
                    surface = pygame.transform.smoothscale(surface = surface, size = (xDim, yDim))  
                    window.blit(surface, (minBorder + xSize * i, minBorder + ySize * j))
                    self.table[j][i].rect = surface.get_rect()
                    self.table[j][i].makeRect(minBorder + xSize * i, minBorder + ySize * j)
        pygame.display.update()

    def checkWin(self):
        for r in self.table:
            for c in r:
                if c.shown == False:
                    return False
        return True

#helper function for quickly making text         
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect) 

#dimensions--width:height = 5:7; width:spaceX = 5:9
#this function assumes that screenheight <= screenwidth]
def setCardScale(screenWidth, screenHeight, minBorder, cols, rows, inBTween):
    screenWidth = screenWidth - minBorder * 2
    screenHeight = screenHeight - minBorder * 2
    dim = 0

    if(cols * 5/screenWidth > rows * 7/screenHeight):#or cols < rows + 2):
        xLength = screenWidth/cols - inBTween
        dim = xLength/250
    else:
        yLength = screenHeight/rows - inBTween
        dim = yLength/350
    #print(dim)
    return dim


def main_menu(): 
    click = False
    while True: 
        screen.fill(black)
        draw_text('main menu', font, (255, 255, 255), screen, 50, 20)
 
        mx, my = pygame.mouse.get_pos()
 
        #Start Game Button
        button_1 = pygame.Rect(50, 100, 200, 50)
        text_1 = font.render("Start Game", True, black)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        pygame.draw.rect(screen, white, button_1)
        text_1Rect = text_1.get_rect()
        text_1Rect.center=button_1.center
        screen.blit(text_1, text_1Rect)
        
        #Options buttons
        button_2 = pygame.Rect(50, 200, 200, 50)
        text_2 = font.render("Options", True, black)
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, white, button_2)
        text_2Rect = text_2.get_rect()
        text_2Rect.center=button_2.center
        screen.blit(text_2, text_2Rect)
        
        #Quit Game Button
        button_3 = pygame.Rect(50, 300, 200, 50)
        text_3 = font.render("Quit Game", True, black)
        if button_3.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, white, button_3)
        text_3Rect = text_3.get_rect()
        text_3Rect.center=button_3.center
        screen.blit(text_3, text_3Rect)
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)  
        
     
def flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, fps, front):
    movedX = 0
    xDimStore = xDim
    xDim, movedX = halfFlip(cards, timeToFlip, movedX, xDim, xDim, yDim, minBorder, xSize, ySize, window, fps, True)        
    for card in cards:     
        if(front):    
            card.show()
        else:
            card.hide()
        card.update()
    
    halfFlip(cards, -timeToFlip, movedX, xDimStore, xDim, yDim, minBorder, xSize, ySize, window, fps, False)
            
def halfFlip(cards, timeToFlip, movedX, maxSize, xDim, yDim, minBorder, xSize, ySize, window, fps, firstHalf):
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
        mainClock.tick(fps)
        xDim -= timeToFlip
        movedX += timeToFlip/2
        for card in cards:
            window.fill(black,rect[i])
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

def game():
    #handles all drawing on the screen 
    cols = 3
    rows = 2
    t = Table(cols, rows, "Tarrot", 2)
    window = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
    
    minBorder = 40
    inBTween = 10
    scale = setCardScale(screenWidth,screenHeight,minBorder, cols, rows, inBTween)
    xDim = 250 * scale
    yDim = 350 * scale
    xSize = xDim + inBTween
    ySize = yDim + inBTween
    fps = 144
    timeToFlip = 8


    t.showAll()
    tempTable = []
    
    for i in range(cols):
            for j in range(rows):
                t.table[j][i].col = i
                t.table[j][i].row = j
                tempTable.append(t.table[j][i])
                surface = t.table[j][i].image.convert()
                surface = pygame.transform.smoothscale(surface = surface, size = (xDim, yDim))  
                #t.table[j][i].image = pygame.transform.(t.table[j][i].image, (xDim, yDim))
                window.blit(surface, (minBorder + xSize * t.table[j][i].col, minBorder + ySize * t.table[j][i].row))
    pygame.display.update()
    
    time.sleep(5)
    
    flip(tempTable, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, fps, False)   
            
    running = True
    while running:
        mainClock.tick(fps)
    
        mouse = pygame.mouse.get_pos()

        window.fill(black, (0,0,200,20)) #so cards show
        draw_text("Lives: " + str(t.lives), lifeFont, white, window, 35, 10)

        if (t.checkWin()):
            
            draw_text("You win!", endFont, green, window, screenWidth / 2, screenHeight / 2)
            pygame.display.update()

            end = True
            while end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = False
                        running = False

        elif (t.lives == 0):
            hiddenTable = []
            for card in tempTable:
                if(not card.shown):
                    hiddenTable.append(card)
            flip(hiddenTable, 3, xDim, yDim, minBorder, xSize, ySize, window, fps, True)

            draw_text("You lose!", endFont, red, window, screenWidth / 2, screenHeight / 2)
            pygame.display.update()

            end = True
            while end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = False
                        running = False

        else:
            t.update()
            #t.drawBoard(window)
            for i in range(cols):
                    for j in range(rows):
                        surface = t.table[j][i].image.convert()
                        surface = pygame.transform.smoothscale(surface = surface, size = (xDim, yDim))  
                        window.blit(surface, (minBorder + xSize * i, minBorder + ySize * j))
                        t.table[j][i].rect = surface.get_rect()
                        t.table[j][i].makeRect(minBorder + xSize * i, minBorder + ySize * j)
            pygame.display.update()


            for row in t.table:
                for c in row:
                    if (c.rect.collidepoint(mouse) and not c.shown):
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                cards = [c]
                                flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, fps, True)

                                #pygame.display.update()
                                
                                t.selection.append(c)
                                if len(t.selection) >= 2:
                                    if not t.checkMatch(timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, fps):
                                        t.lives = t.lives - 1
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        t.update()
        pygame.display.update()
    
main_menu()


"""
import pygame, sys
import random
import time

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
screenWidth = 1200
screenHeight = 950
screen = pygame.display.set_mode((screenWidth, screenHeight),0,32)

font = pygame.font.SysFont(None, 20)
lifeFont = pygame.font.SysFont('Times New Roman', 20)
endFont = pygame.font.SysFont('Times New Roman', 32)

green = (0, 255, 0)
red = (255, 0, 0)
white (255, 255, 255)
black = (0, 0, 0)

click = False

class Card():
    def __init__(self, theme, ID):
        super().__init__()

        self.ID = ID

        folder = "theme_" + str(theme) + "/"
        img = str(ID) + ".jpg"

        path = (folder + img)
        try:
            self.front_image = pygame.image.load(path)
        except FileNotFoundError:
            self.front_image = pygame.image.load(folder + "default.jpg") 
            
        self.back_image = pygame.image.load(folder + "50.jpg")
    
        self.image = self.back_image
        self.rect = self.image.get_rect()
        self.shown = False

    def update(self):
        if self.shown: 
            self.image = self.front_image
        else:
            self.image = self.back_image
    
    # Boolean for showing up or not
    def show(self):
        self.shown = True
    
    
    def hide(self):
        self.shown = False

    def makeRect(self, x, y):
        self.rect.topleft = (x, y)
    
class Table():
    def __init__(self, x, y, theme, lives):
        self.theme = theme
        self.lives = lives
        self.x = x
        self.y = y
        self.table = [[0 for i in range(x)] for j in range(y)]
        self.selection = []
        self.createTable() 
      
    #Creates the randomized table of pairs, used internally when the table is made
    def createTable(self):
        uniqueCards = int(self.x * self.y / 2)
        cards = []
        for c in range(uniqueCards):
            cards.append(Card(self.theme, c))
            cards.append(Card(self.theme, c))
            
        random.shuffle(cards)
        count = 0
        for i in range(self.y):
            for j in range(self.x):
                self.table[i][j] = cards[count]
                count = count + 1

    #Shows all cards, waits five seconds, hides all cards
    def showAll(self):
        for r in self.table:
            for c in r:
                c.show()
                c.update()
        
    def hideAll(self):
        for r in self.table:
            for c in r:
                c.hide()
                c.update()

    def update(self):
        for r in self.table:
            for c in r:
                c.update()

    def checkMatch(self):
        if self.selection[0].ID == self.selection[1].ID:
            self.selection.clear()
            return True
        else:
            time.sleep(1)
            self.selection[0].hide()
            self.selection[1].hide()
            self.selection.clear()
            return False

    def drawBoard(self, window):
        self.update()
        for i in range(4):
            for j in range(3):
                window.blit(t.table[j][i].image, (25 + (140 * i), 25 + (190 * j)))
                t.table[j][i].makeRect(25 + (140 * i), 25 + (190 * j))
        pygame.display.update()

    def checkWin(self):
        for r in self.table:
            for c in r:
                if c.shown == False:
                    return False
        return True

#helper function for quickly making text         
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect) 

#dimensions--width:height = 5:7; width:spaceX = 5:9
#this function assumes that screenheight <= screenwidth]
def setCardScale(screenWidth, screenHeight, minBorder, cols, rows, inBTween):
    screenWidth = screenWidth - minBorder * 2
    screenHeight = screenHeight - minBorder * 2
    dim = 0

    if(cols/rows > screenWidth/screenHeight):
        xLength = screenWidth/cols - inBTween
        dim = xLength/250
    else:
        yLength = screenHeight/rows - inBTween
        dim = yLength/350
    print(dim)
    return dim

def main_menu(): 
    while True: 
        screen.fill((0,0,0))
        draw_text('main menu', font, (255, 255, 255), screen, 20, 20)
 
        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(50, 100, 200, 50)
        button_2 = pygame.Rect(50, 200, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)     

def game():
    #handles all drawing on the screen 
    cols = 8
    rows = 8
    t = Table(cols, rows, "test", 3)
    window = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)

    minBorder = 40
    inBTween = 10
    scale = setCardScale(screenWidth,screenHeight,minBorder, cols, rows, inBTween)
    xDim = 250 * scale
    yDim = 350 * scale
    xSize = xDim + inBTween
    ySize = yDim + inBTween

    t.showAll()

    for i in range(cols):
            for j in range(rows):
                t.table[j][i].image = pygame.transform.smoothscale(t.table[j][i].image, (xDim, yDim))
                window.blit(t.table[j][i].image, (minBorder + xSize * i, minBorder + ySize * j))
    pygame.display.update()

    time.sleep(3)

    t.hideAll()
    pygame.display.update()


    running = True
    while running:
        mainClock.tick(144)
    
        mouse = pygame.mouse.get_pos()

        window.fill(black)
        draw_text("Lives: " + str(t.lives), lifeFont, white, 35, 10)

        if (t.checkWin()):
            t.update()
            t.drawBoard(window)

            draw_text("You win!", endFont, green, screenWidth / 2, screenHeight / 2)
            pygame.display.update()

            end = True
            while end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = False
                        running = False

        elif (t.lives == 0):
            t.showAll()
            t.drawBoard(window)

            draw_text("You lose!", endFont, red, screenWidth / 2, screenHeight / 2)
            pygame.display.update()

            end = True
            while end:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        end = False
                        running = False

        else:
            t.update()
            t.drawBoard(window)

            if len(t.selection) >= 2:
                if not t.checkMatch():
                    t.lives = t.lives - 1

            for row in t.table:
                for c in row:
                    if (c.rect.collidepoint(mouse) and not c.shown):
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                c. show()
                                c.update()
                                pygame.display.update()
                                t.selection.append(c)

                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        t.update()
        pygame.display.update()
    
    main_menu()
"""