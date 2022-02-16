# -*- coding: utf-8 -*-

import pygame
import sys
from Table import Table
import time
from Animations import Animations
import pygame_menu
from pygame.locals import *
from pygame import mixer


class Game():
    screen = None
    def __init__(self):
        self.volume = int(self.readSettingFromFile("volume"))
        self.selectedTheme = self.readCardTheme()
        self.FPS = int(self.readSettingFromFile("FPS"))
        self.screenWidth = int(self.readSettingFromFile("screenWidth"))
        self.screenHeight = int(self.readSettingFromFile("screenHeight"))
        self.mainClock = pygame.time.Clock()
        self.animate = Animations(self.FPS)
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

        if (cols * 5 / screenWidth > rows * 7 / screenHeight):  # or cols < rows + 2):
            xLength = screenWidth / cols - inBTween
            dim = xLength / 250
        else:
            yLength = screenHeight / rows - inBTween
            dim = yLength / 350
        return dim

    def readSettingFromFile(self, sName):
        file = open("SavedVariables.txt")
        string = None
        for line in file:
            if (line.startswith(sName)):
                string = line
                break
        string = string.replace(sName + "=", "")
        string = string.replace("\n", "")
        file.close()
        return string

    def saveSettingToFile(self, sName, sValue):
        file = open("SavedVariables.txt", "r")
        settings = []
        for line in file:
            if (line.startswith(sName)):
                oldVal = line.replace(sName + "=", "")
                line = line.replace(oldVal, sValue)
            if (line != "\n"):
                settings.append(line)
        file.close()
        print(settings)
        file = open("SavedVariables.txt", "w")
        for setting in settings:
            file.write(setting + "\n")
        file.close()

    def readCardTheme(self):
        InitialCardSetting = self.readSettingFromFile("selectedTheme")
        InitialCardSetting = InitialCardSetting.replace("theme_", "")
        print(InitialCardSetting)
        return InitialCardSetting

    # not perfect: deletes whole file!
    def saveInitialCardTheme(self, newTheme):
        self.selectedTheme = newTheme
        newTheme = "theme_" + newTheme
        self.saveSettingToFile("selectedTheme", newTheme)

    def options(self, screen):
        optionsMenu = screen
        # This function has a lot about it that doesn't make sense, but it seems to need to be this way

        menuTheme = pygame_menu.themes.Theme(
            background_color=(202, 228, 241),
            title_background_color=(0, 0, 0, 0),
        )

        menu = pygame_menu.Menu(
            title="",
            height=self.screenHeight,
            width=self.screenWidth,
            theme=menuTheme)

        def setCardTheme(newThemeName, newThemeNameButLike___Again, **kwargs):
            # global selectedTheme
            value_tuple, index = newThemeName
            # selectedTheme = value_tuple[0]
            self.saveInitialCardTheme(value_tuple[0])

        allCardThemes = [('Tarrot', 'Tarrot'),
                         ('Pokemon', 'Pokemon'),
                         ('Mario', 'Mario'),
                         ('Poker', 'Poker')]
        themeSelector = menu.add.dropselect(
            title="Deck Theme",
            items=allCardThemes,
            # placeholder=allThemes[defaultCardTheme][0],
            onchange=setCardTheme,
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            # selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder=self.selectedTheme,
            placeholder_add_to_selection_box=False
        )

        def setDifficulty(difficulty, difficultyIndex, **kwargs):
            # global selectedTheme
            value_tuple, index = difficulty
            # selectedTheme = value_tuple[0]
            #self.saveInitialCardTheme(value_tuple[0])

        allDificulties = [('Easy', 0),
                          ('Medium', 1),
                          ('Hard', 2)]
        difficultySelector = menu.add.dropselect(
            title="Difficulty",
            items=allDificulties,
            # placeholder=allThemes[defaultCardTheme][0],
            onchange=setDifficulty,
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            # selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder='Medium',
            placeholder_add_to_selection_box=False
        )

        def setResolution(newRes, resX, resY, **kwargs):
            global screen
            value_tuple, index = newRes
            self.screenWidth = resX
            self.screenHeight = resY
            screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)
            menu.resize(resX, resY)
            self.saveSettingToFile("screenWidth", str(resX))
            self.saveSettingToFile("screenHeight", str(resY))

            # selectedTheme = value_tuple[0]
            #self.saveInitialCardTheme(value_tuple[0])

        allResolutions = [('1280 x 950', 1280, 950),
                          ('1000 x 1000', 1000, 1000),
                          ('650 x 480', 650, 480),
                          ('Full Screen', 1200, 700)]
        resolutionSelector = menu.add.dropselect(
            title="Resolution",
            items=allResolutions,
            # placeholder=allThemes[defaultCardTheme][0],
            onchange=setResolution,
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            # selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder= str(self.screenWidth) + " x " + str(self.screenHeight),
            placeholder_add_to_selection_box=False
        )

        def setFPS(newFPSData, newFPSNum, **kwargs):
            # global selectedTheme
            value_tuple, index = newFPSData
            # selectedTheme = value_tuple[0]
            self.FPS = newFPSNum
            self.animate.frames = newFPSNum
            self.saveSettingToFile("FPS", value_tuple[0])

        allFPS = [('360', 360),
                  ('140', 140),
                  ('60', 60),
                  ('30', 30),
                  ('Custom', 360)]
        fpsSelector = menu.add.dropselect(
            title="Frame Rate",
            items=allFPS,
            # placeholder=allThemes[defaultCardTheme][0],
            onchange=setFPS,
            scrollbar_thick=5,
            selection_option_font=self.lifeFont,
            # selection_box_border_color=(0,0,0,0),
            selection_box_width=250,
            selection_box_height=250,
            placeholder=str(self.FPS),
            placeholder_add_to_selection_box=False
        )


        def set_vol(range, **kwargs):
            val = int(range)
            self.volume = int(val)
            mixer.music.set_volume(self.volume/100)
            self.saveSettingToFile("volume", str(val))
            #set volume of mixer takes value only from 0 to 1, val is divided by 100

        volumeSlider = menu.add.range_slider(
            title="Volume",
            default=self.volume,
            range_values=(0, 100),
            increment=1,
            onchange = set_vol,
            value_format=lambda x: str(int(x)),
           # command = set_vol()
        )

        themeSelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        difficultySelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        resolutionSelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        fpsSelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
        volumeSlider.add_self_to_kwargs()  # Callbacks will receive widget as parameter

        # running = True
        while True:
            optionsMenu.fill(self.black)
            self.draw_text_center(
                "Press escape to go back to main menu",
                self.lifeFont, self.white,
                self.screenWidth / 2, self.screenHeight / 6,
                optionsMenu
            )
            events = pygame.event.get()
            # events2 = pygame.event.get()
            menu.draw(optionsMenu)
            menu.update(events)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            pygame.display.update()
            self.mainClock.tick(self.FPS)

    def main_menu(self):
        global screen
        screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)

        titleFont = pygame.font.Font("assets/font.ttf", 50)
        font = pygame.font.SysFont(None, 20)

        # Main Menu Music
        mixer.init()
        mixer.music.load('Sounds/mainmenu.mp3')
        mixer.music.set_volume(self.volume/100)
        mixer.music.play(-1)

        white = (255, 255, 255)
        black = (0, 0, 0)

        click = False
        while True:
            screen.fill((202, 228, 241))
            self.draw_text_center('Place Holder', titleFont, white,  self.screenWidth / 2, self.screenHeight / 6, screen)
            self.draw_text_center('Title', titleFont, white,  self.screenWidth / 2, self.screenHeight / 4, screen)

            mx, my = pygame.mouse.get_pos()

            # Start Game Button
            butHalfX = 100
            button_1 = pygame.Rect(self.screenWidth/2 - butHalfX, self.screenHeight*3/8, 200, 50)
            text_1 = font.render("Start Game", True, black)
            if button_1.collidepoint((mx, my)):
                if click:
                    pygame.mixer.music.stop()
                    screen.fill(black)
                    if self.game(screen, 1000000):
                        pygame.quit()
                        sys.exit()
            pygame.draw.rect(screen, white, button_1)
            text_1Rect = text_1.get_rect()
            text_1Rect.center = button_1.center
            screen.blit(text_1, text_1Rect)

            # Options buttons
            button_2 = pygame.Rect(self.screenWidth/2 - butHalfX, self.screenHeight*4/8, 200, 50)
            text_2 = font.render("Options", True, black)
            if button_2.collidepoint((mx, my)):
                if click:
                    mixer.init()
                    mixer.music.load('Sounds/settings.mp3')
                    mixer.music.set_volume(self.volume/100)
                    mixer.music.play(-1)
                    self.options(screen)
            pygame.draw.rect(screen, white, button_2)
            text_2Rect = text_2.get_rect()
            text_2Rect.center = button_2.center
            screen.blit(text_2, text_2Rect)

            # Quit Game Button
            button_3 = pygame.Rect(self.screenWidth/2 - butHalfX, self.screenHeight*5/8, 200, 50)
            text_3 = font.render("Quit Game", True, black)
            if button_3.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()
            pygame.draw.rect(screen, white, button_3)
            text_3Rect = text_3.get_rect()
            text_3Rect.center = button_3.center
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
            self.mainClock.tick(self.FPS)
            
    def centerDeckX(self, xSize, col, screenWidth, minBorder):
        deckX = xSize * col
        availableSpace = screenWidth - minBorder * 2
        toXCenter = availableSpace - deckX
        toXCenter /= 2
        return toXCenter
        
    def game(self, window, matchTime):
        window.fill(self.black)
        t = self.createTable(1)

        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        black = (0, 0, 0)

        buttonFont = pygame.font.SysFont('Times New Roman', 20)
        lifeFont = pygame.font.SysFont('Times New Roman', 20)
        endFont = pygame.font.SysFont('Times New Roman', 32)

        minBorder = 70
        inBTween = 10
        scale = self.setCardScale(minBorder, t.x, t.y, inBTween)
        xDim = int(250 * scale)
        yDim = int(350 * scale)
        xSize = xDim + inBTween
        ySize = yDim + inBTween
        toXCenter = self.centerDeckX(xSize, t.x, self.screenWidth, minBorder)
        timeToFlip = int(3000 * scale)  # can't be too fast or frames don't register

        t.showAll()
        tempTable = []
        for i in range(t.x):
            for j in range(t.y):
                t.table[j][i].col = i
                t.table[j][i].row = j
                tempTable.append(t.table[j][i])
                surface = t.table[j][i].image.convert()
                surface = pygame.transform.scale(surface, (xDim, yDim))
                window.blit(surface, ((minBorder + toXCenter) + xSize * t.table[j][i].col, minBorder + ySize * t.table[j][i].row))
        pygame.display.update()

        time.sleep(2)
        self.animate.flip(tempTable, timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, False)

        timer = matchTime
        sTime = time.time()

        timeLeft = int(timer - (time.time() - sTime))

        streak = 0

        running = True
        quitG = False
        while running:
            self.mainClock.tick(self.FPS)

            mouse = pygame.mouse.get_pos()

            window.fill(black, (0, 0, 400, 40))  # so cards show during lose screen
            self.draw_text("Lives: " + str(t.lives), lifeFont, white, 5, 0, window)
            self.draw_text("Time: " + str(timeLeft) + "s", lifeFont, white, 5, 18, window)
            self.draw_text("Score: " + str(t.score), lifeFont, white, 105, 0, window)

            if (t.checkWin(timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window)):
                window.fill(black, (0, 0, 400, 40))

                if len(t.selection) >= 2:
                    t.score = t.score + 100 + (50 * streak)

                t.score = t.score + (timeLeft)
                t.score = t.score + (t.lives * 100)

                self.draw_text("Lives: " + str(t.lives), lifeFont, white, 5, 0, window)
                self.draw_text("Time: " + str(timeLeft) + "s", lifeFont, white, 5, 18, window)
                self.draw_text("Score: " + str(t.score), lifeFont, white, 105, 0, window)

                self.draw_text_center("You win!", endFont, green, self.screenWidth / 2, self.screenHeight / 2, window)

                mixer.init()
                mixer.music.load('Sounds/winner.mp3')
                mixer.music.set_volume(self.volume/100)
                mixer.music.play()

                running, quitG, playAgain = self.endScreen(window)

                if playAgain:
                    pygame.mixer.music.stop()
                    return Game.game(self, window, matchTime)

            elif (t.lives == 0 or timeLeft <= 0):
                hiddenTable = []
                for card in tempTable:
                    if (not card.shown):
                        hiddenTable.append(card)

                self.animate.flip(hiddenTable, 1000, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, True)

                self.draw_text_center("You lose!", endFont, red, self.screenWidth / 2, self.screenHeight / 2, window)
                mixer.init()
                mixer.music.load('Sounds/gameover.mp3')
                mixer.music.play()

                running, quitG, playAgain = self.endScreen(window)

                if playAgain:
                    pygame.mixer.music.stop()
                    return Game.game(self, window, matchTime)

            else:
                t.update()
                for i in range(t.x):
                    for j in range(t.y):
                        surface = t.table[j][i].image.convert()
                        surface = pygame.transform.smoothscale(surface, (xDim, yDim))
                        t.table[j][i].rect = surface.get_rect()
                        t.table[j][i].makeRect((minBorder + toXCenter) + xSize * i, minBorder + ySize * j)
                pygame.display.update()

                timeLeft = int(timer - (time.time() - sTime))

                if len(t.selection) >= 1:
                    t.checkBomb(timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window)
                    if len(t.selection) >= 2:
                        if not t.checkMatch(timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window):
                            t.lives = t.lives - 1
                            streak = 0
                        else:
                            t.score = t.score + 100 + (50 * streak)
                            streak = streak + 1

                for row in t.table:
                    for c in row:
                        if (c.rect.collidepoint(mouse) and not c.shown):
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    cards = [c]
                                    self.animate.flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window,
                                                      True)

                                    t.selection.append(c)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quitG = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

        pygame.mixer.music.stop()
        return quitG

    def endScreen(self, window):
        retryButton = pygame.Rect((self.screenWidth / 2) - 100, (self.screenHeight / 2) + 50, 200, 50)
        retryButtonText = self.buttonFont.render("Press R to Restart", True, self.black)
        pygame.draw.rect(window, (127, 127, 127), retryButton)
        retryButtonTextRect = retryButtonText.get_rect()
        retryButtonTextRect.center = retryButton.center
        window.blit(retryButtonText, retryButtonTextRect)
        pygame.display.update()

        while True:
            self.mainClock.tick(self.FPS)
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return [False, True, False]  # [Running, quitgame, playagain]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return [False, False, False]
                    if event.key == pygame.K_r:
                        window.fill(self.black)  # so cards show during lose screen
                        return [False, False, True]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retryButton.collidepoint(mouse):
                        window.fill(self.black)
                        return [False, False, True]
                    
    def createTable(self, difficulty):
        if difficulty == 0:
            return Table(4, 3, self.selectedTheme, 5, difficulty, self.FPS)
        elif difficulty == 1:
            return Table(5, 5, self.selectedTheme, 10, difficulty, self.FPS)
        else:
            return Table(5, 5, self.selectedTheme, 6, difficulty, self.FPS)