# -*- coding: utf-8 -*-

import pygame
import sys
from Table import Table
import time
from Animations import Animations
import pygame_menu

class Game():
    def __init__(self, screenWidth, screenHeight):
        self.selectedTheme = self.readInitialCardTheme()
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.mainClock = pygame.time.Clock()
        self.animate = Animations()
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.buttonFont = pygame.font.SysFont('Times New Roman', 20)
        self.lifeFont = pygame.font.SysFont('Times New Roman', 20)
        self.endFont = pygame.font.SysFont('Times New Roman', 32)
    
    def draw_text(self, text, font, color, x, y, window):
        img = font.render(text, True, color)
        textRect = img.get_rect()
        textRect.topleft = (x, y)
        window.blit(img, textRect)

    def draw_text_center(self, text, font, color, x, y, window):
        img = font.render(text, True, color)
        textRect = img.get_rect()
        textRect.center = (x, y)
        window.blit(img, textRect)
    
    def setCardScale(self, minBorder, cols, rows, inBTween):
        screenWidth = self.screenWidth - minBorder * 2
        screenHeight = self.screenHeight - minBorder * 2
        dim = 0
    
        if(cols * 5/screenWidth > rows * 7/screenHeight):#or cols < rows + 2):
            xLength = screenWidth/cols - inBTween
            dim = xLength/250
        else:
            yLength = screenHeight/rows - inBTween
            dim = yLength/350
            
        return dim
    
    #these read and write files could be toolified for more read and write variables
    def readInitialCardTheme(self):
        file = open("SavedVariables.txt")
        string = None
        for line in file:
            if(line.startswith("selectedTheme")):
                string = line
                break
        string = string.replace("selectedTheme=theme_","")
        print(string)
        file.close()
        return string


    #not perfect: deletes whole file!
    def saveInitialCardTheme(self, newTheme):
        #file = open("SavedVariables.txt", "r")
        #string = self.readInitialCardTheme()
        #file.close()
        file = open("SavedVariables.txt", "w")
        self.selectedTheme = newTheme
        file.write("selectedTheme=theme_"+self.selectedTheme)
        
    def options(self):
        
        global selectedTheme
        optionsMenu = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)
        #This function has a lot about it that doesn't make sense, but it seems to need to be this way
        def setTheme(newThemeName, newThemeIndex, **kwargs):
            #global selectedTheme
            value_tuple, index = newThemeName
            #selectedTheme = value_tuple[0]
            self.saveInitialCardTheme(value_tuple[0])
            
        
        menuTheme = pygame_menu.themes.Theme(
            background_color=(0,0,0,0),
            title_background_color = (0,0,0,0),
            )
        
        menu = pygame_menu.Menu(
            title="", 
            height=self.screenHeight, 
            width=self.screenWidth,
            theme=menuTheme)
        
        allThemes = [('Tarrot', 'Tarrot'),
                 ('Pokemon', 'Pokemon'),
                 ('Mario', 'Mario'),
                 ('Poker', 'Poker')]
        
        themeSelector = menu.add.dropselect(
            title="Deck Theme",
            items=allThemes,
            #placeholder=allThemes[defaultCardTheme][0],
            onchange=setTheme, 
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            #selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder=self.selectedTheme,
            placeholder_add_to_selection_box=False
        )
        difficultySelector = menu.add.dropselect(
            title="Diffuclty",
            items=allThemes,
            #placeholder=allThemes[defaultCardTheme][0],
            onchange=setTheme, 
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            #selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder=self.selectedTheme,
            placeholder_add_to_selection_box=False
        )
        resolutionSelector = menu.add.dropselect(
            title="Resolution",
            items=allThemes,
            #placeholder=allThemes[defaultCardTheme][0],
            onchange=setTheme, 
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            #selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder=self.selectedTheme,
            placeholder_add_to_selection_box=False
        )
        fpsSelector = menu.add.dropselect(
            title="Frame Rate",
            items=allThemes,
            #placeholder=allThemes[defaultCardTheme][0],
            onchange=setTheme, 
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            #selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder=self.selectedTheme,
            placeholder_add_to_selection_box=False
        )
        fullScreenSelector = menu.add.dropselect(
            title="Full Screen",
            items=allThemes,
            #placeholder=allThemes[defaultCardTheme][0],
            onchange=setTheme, 
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            #selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder=self.selectedTheme,
            placeholder_add_to_selection_box=False
        )
        volumeSelector = menu.add.dropselect(
            title="Volume",
            items=allThemes,
            #placeholder=allThemes[defaultCardTheme][0],
            onchange=setTheme, 
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            #selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder=self.selectedTheme,
            placeholder_add_to_selection_box=False
        )

        
        themeSelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        difficultySelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        resolutionSelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        fpsSelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        fullScreenSelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        volumeSelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        
        
        #running = True
        while True: 
            optionsMenu.fill(self.black)
            self.draw_text_center(
                "Press escape to go back to main menu", 
                self.lifeFont, self.white, 
                self.screenWidth/2, self.screenHeight/6,
                optionsMenu
                )
            events = pygame.event.get()
            #events2 = pygame.event.get()
            menu.draw(optionsMenu)
            menu.update(events)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            pygame.display.update()
            self.mainClock.tick(60) 
            
    def main_menu(self):
        screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)
        
        font = pygame.font.SysFont(None, 20)
        
        white = (255, 255, 255)
        black = (0, 0, 0)
        
        click = False
        while True: 
            screen.fill(black)
            self.draw_text('main menu', font, white, 50, 20, screen)
     
            mx, my = pygame.mouse.get_pos()
     
            #Start Game Button
            button_1 = pygame.Rect(50, 100, 200, 50)
            text_1 = font.render("Start Game", True, black)
            if button_1.collidepoint((mx, my)):
                if click:
                    screen.fill(black)
                    if self.game(screen, 3, 3, 10, 1000000, 0):
                        pygame.quit()
                        sys.exit()
            pygame.draw.rect(screen, white, button_1)
            text_1Rect = text_1.get_rect()
            text_1Rect.center=button_1.center
            screen.blit(text_1, text_1Rect)
            
            #Options buttons
            button_2 = pygame.Rect(50, 200, 200, 50)
            text_2 = font.render("Options", True, black)
            if button_2.collidepoint((mx, my)):
                if click:
                    self.options()
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
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
     
            pygame.display.update()
            self.mainClock.tick(60)
    
    def game(self, window, x, y, lives, matchTime, score):
        window.fill(self.black) 
        t = Table(x, y, self.selectedTheme, lives, 0, self.mainClock)#, 0)
        
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        black = (0, 0, 0)
        
        buttonFont = pygame.font.SysFont('Times New Roman', 20)
        lifeFont = pygame.font.SysFont('Times New Roman', 20)
        endFont = pygame.font.SysFont('Times New Roman', 32)
        
        minBorder = 40
        inBTween = 10
        scale = self.setCardScale(minBorder, x, y, inBTween)
        xDim = int(250 * scale)
        yDim = int(350 * scale)
        xSize = xDim + inBTween
        ySize = yDim + inBTween
        timeToFlip = int(40 * scale) #can't be too fast or frames don't register
        
        t.showAll()
        tempTable = []
        for i in range(x):
                for j in range(y):
                    t.table[j][i].col = i
                    t.table[j][i].row = j
                    tempTable.append(t.table[j][i])
                    surface = t.table[j][i].image.convert()
                    surface = pygame.transform.scale(surface, (xDim, yDim))
                    window.blit(surface, (minBorder + xSize * t.table[j][i].col, minBorder + ySize * t.table[j][i].row))
        pygame.display.update()
        
        time.sleep(2)        
        self.animate.flip(tempTable, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, False)
        
        timer = matchTime
        sTime = time.time()

        timeLeft = int(timer - (time.time() - sTime))
        
        click = False
        running = True
        quitG = False
        while running:
            self.mainClock.tick(60)
            
            mouse = pygame.mouse.get_pos()    
            
            window.fill(black, (0,0,200,40)) #so cards show during lose screen
            self.draw_text("Lives: " + str(t.lives), lifeFont, white, 5, 0, window)
            self.draw_text("Time: " + str(timeLeft) + "s", lifeFont, white, 5, 18, window)
            #self.draw_text("Score: " + str(t.score), lifeFont, white, 105, 0, window)
            
            if (t.checkWin()):
                self.draw_text_center("You win!", endFont, green, self.screenWidth / 2, self.screenHeight / 2, window)
                
                running, quitG, playAgain = self.endScreen(window)
                
                if playAgain:
                    return Game.game(self, window, x, y, lives, matchTime, score)
                            
            elif (t.lives == 0 or timeLeft <= 0):
                hiddenTable = []
                for card in tempTable:
                    if (not card.shown):
                        hiddenTable.append(card)
                        
                self.animate.flip(hiddenTable, 3, xDim, yDim, minBorder, xSize, ySize, window, True)
                                
                self.draw_text_center("You lose!", endFont, red, self.screenWidth / 2, self.screenHeight / 2, window)
                
                
                running, quitG, playAgain = self.endScreen(window)
                
                if playAgain:
                    return Game.game(self, window, x, y, lives, matchTime, score)
            
            else:
                t.update()
                for i in range(x):
                    for j in range(y):
                        surface = t.table[j][i].image.convert()
                        surface = pygame.transform.smoothscale(surface, (xDim, yDim))  
                        t.table[j][i].rect = surface.get_rect()
                        t.table[j][i].makeRect(minBorder + xSize * i, minBorder + ySize * j)
                pygame.display.update()
            
                timeLeft = int(timer - (time.time() - sTime))
            
                if len(t.selection) >= 1:
                    t.checkBomb(timeToFlip, xDim, yDim, minBorder, xSize, ySize, window)
                    if len(t.selection) >= 2:
                        if not t.checkMatch(timeToFlip, xDim, yDim, minBorder, xSize, ySize, window):
                            t.lives = t.lives - 1
                        #else:
                            #t.score = t.score + 100
                for row in t.table:
                    for c in row:
                        if (c.rect.collidepoint(mouse) and not c.shown):
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    cards = [c]
                                    self.animate.flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, True)
                                    t.selection.append(c)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quitG = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        
        return quitG
    
    def endScreen(self, window):
        retryButton = pygame.Rect((self.screenWidth / 2) - 100, (self.screenHeight / 2) + 50, 200, 50)
        retryButtonText = self.buttonFont.render("Press R to Restart", True, self.black)
        pygame.draw.rect(window, (127,127,127), retryButton)
        retryButtonTextRect = retryButtonText.get_rect()
        retryButtonTextRect.center=retryButton.center
        window.blit(retryButtonText, retryButtonTextRect)
        pygame.display.update()
        
        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return [False, True, False] #[Running, quitgame, playagain]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return [False, False, False]
                    if event.key == pygame.K_r: 
                        window.fill(self.black) #so cards show during lose screen
                        return [False, False, True]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retryButton.collidepoint(mouse):
                        window.fill(self.black)
                        return [False, False, True]