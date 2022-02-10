# -*- coding: utf-8 -*-

import pygame
import sys
from Table import Table
import time
from Animations import Animations

class Game():
    def __init__(self, screenWidth, screenHeight):
        self.screenWidth = screenHeight
        self.screenHeight = screenHeight
        self.mainClock = pygame.time.Clock()
        self.animate = Animations(self.mainClock)
    
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
                    if self.game(screen, 5, 5, "Mario", 10, 45):
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
    
    def game(self, window, x, y, theme, lives, matchTime):
        t = Table(x, y, theme, lives, 0, self.mainClock)
        
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        black = (0, 0, 0)
        
        lifeFont = pygame.font.SysFont('Times New Roman', 20)
        endFont = pygame.font.SysFont('Times New Roman', 32)
        
        minBorder = 40
        inBTween = 10
        scale = self.setCardScale(minBorder, x, y, inBTween)
        xDim = int(250 * scale)
        yDim = int(350 * scale)
        xSize = xDim + inBTween
        ySize = yDim + inBTween
        timeToFlip = 8
        
        t.showAll()
        tempTable = []
        
        for i in range(x):
                for j in range(y):
                    t.table[j][i].col = i
                    t.table[j][i].row = j
                    tempTable.append(t.table[j][i])
                    surface = t.table[j][i].image.convert()
                    img = pygame.transform.smoothscale(surface, (xDim, yDim))
                    window.blit(img, (minBorder + xSize * t.table[j][i].col, minBorder + ySize * t.table[j][i].row))
        pygame.display.update()
        
        time.sleep(2)
        
        self.animate.flip(tempTable, timeToFlip, xDim, yDim, minBorder, xSize, ySize, window, False)
        
        timer = matchTime
        sTime = time.time()

        timeLeft = int(timer - (time.time() - sTime))
        
        running = True
        quitG = False
        while running:
            self.mainClock.tick(60)
            
            mouse = pygame.mouse.get_pos()    
            
            window.fill(black)
            self.draw_text("Lives: " + str(t.lives), lifeFont, white, 5, 0, window)
            self.draw_text("Time: " + str(timeLeft) + "s", lifeFont, white, 5, 18, window)
            
            if (t.checkWin()):
                t.update()
                
                self.draw_text_center("You win!", endFont, green, self.screenWidth / 2, self.screenHeight / 2, window)
                pygame.display.update()
                
                end = True
                while end:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            end = False
                            running = False
                            quitG = True
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
                
            elif (t.lives == 0 or timeLeft <= 0):
                hiddenTable = []
                for card in tempTable:
                    if (not card.shown):
                        hiddenTable.append(card)
                        
                self.animate.flip(hiddenTable, 3, xDim, yDim, minBorder, xSize, ySize, window, True)
                                
                self.draw_text_center("You lose!", endFont, red, self.screenWidth / 2, self.screenHeight / 2, window)
                pygame.display.update()
                
                end = True
                while end:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            end = False
                            running = False
                            quitG = True
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                running = False
            
            else:
                t.update()
                for i in range(x):
                    for j in range(y):
                        surface = t.table[j][i].image.convert()
                        img = pygame.transform.smoothscale(surface, (xDim, yDim))  
                        window.blit(img, (minBorder + xSize * i, minBorder + ySize * j))
                        t.table[j][i].rect = img.get_rect()
                        t.table[j][i].makeRect(minBorder + xSize * i, minBorder + ySize * j)
                pygame.display.update()
            
                timeLeft = int(timer - (time.time() - sTime))
            
                if len(t.selection) >= 1:
                    t.checkBomb(timeToFlip, xDim, yDim, minBorder, xSize, ySize, window)
                    if len(t.selection) >= 2:
                        if not t.checkMatch(timeToFlip, xDim, yDim, minBorder, xSize, ySize, window):
                            t.lives = t.lives - 1
                
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
    
