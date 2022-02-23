# -*- coding: utf-8 -*-

import pygame
import sys
from Table import Table
import time
from Animations import Animations
from Button import Button
import pygame_menu
from pygame.locals import *
from pygame import mixer
import threading
import keyboard #must be installed: pip install keyboard in anaconda cmd
from Score import Score

running = True

class Game():
    def __init__(self):
        #multiplayer-----------#eventually will be read from File; some variables still need to be saved by the functions in multiplayerOptions
        self.teamCount = 0 #how many teams
        self.playerCount = 2 #how many players
        self.playersInTeams = [] #if there is a team with 0 players, then that team does not exist according to the user
        self.lives = 4 #how many lives per team; may add switch to select lives per player or lives per team
        self.error = False #set to true when there is any user error; this will not let the user exit the menu until they fix the error
        #singlePlayer-----------
        self.difficulty = int(self.readSettingFromFile("SavedVariables.txt", "difficulty"))
        self.gamemode = int(self.readSettingFromFile("SavedVariables.txt", "gamemode"))
        #both----------
        self.flipTime = 2 #
        self.volume = int(self.readSettingFromFile("SavedVariables.txt", "volume"))
        self.selectedTheme = self.readCardTheme()
        self.FPS = int(self.readSettingFromFile("SavedVariables.txt", "FPS"))
        self.screenWidth = int(self.readSettingFromFile("SavedVariables.txt", "screenWidth"))
        self.screenHeight = int(self.readSettingFromFile("SavedVariables.txt", "screenHeight"))
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

    def saveSettingToFile(self, fName, sName, sValue):
        file = open(fName, "r")
        settings = []
        for line in file:
            if (line.startswith(sName)):
                oldVal = line.replace(sName + "=", "")
                line = line.replace(oldVal, sValue)
            if (line != "\n"):
                settings.append(line)
        file.close()
        print(settings)
        file = open(fName, "w")
        for setting in settings:
            file.write(setting + "\n")
        file.close()

    def readCardTheme(self):
        InitialCardSetting = self.readSettingFromFile("SavedVariables.txt", "selectedTheme")
        InitialCardSetting = InitialCardSetting.replace("theme_", "")
        print(InitialCardSetting)
        return InitialCardSetting

    def saveInitialCardTheme(self, newTheme):
        self.selectedTheme = newTheme
        newTheme = "theme_" + newTheme
        self.saveSettingToFile("SavedVariables.txt", "selectedTheme", newTheme)
        
    def sOrMOptions(self, screen):
        optionsMenu = screen
        menuTheme = pygame_menu.themes.Theme(
            background_color=(202, 228, 241),
            title_background_color=(202, 228, 241),
        )
        
        menu = pygame_menu.Menu(
            title="",
            height=self.screenHeight,
            width=self.screenWidth,
            columns=2,
            rows=2,
            theme=menuTheme)
        
        def singlePlayer(**kwargs):
            self.game(screen)
            #self.main_menu()#returns to main menu instead of options menu
        
        playSBut = menu.add.button('Single-Player', singlePlayer)
        playSBut.add_self_to_kwargs()
        
        def singlePlayerOptionsButton(**kwargs):
            self.singlePlayerOptions(screen)
        
        optionsSBut = menu.add.button('Single-Player Options', singlePlayerOptionsButton)
        optionsSBut.add_self_to_kwargs()
        
        def multiPlayer(**kwargs):
            self.game(screen)
            #self.main_menu()#returns to main menu instead of options menu
        
        playMBut = menu.add.button('Multi-Player', multiPlayer)
        playMBut.add_self_to_kwargs()
        
        def multiPlayerOptionsButton(**kwargs):
            self.multiplayerOptions(screen)
        
        optionsMBut = menu.add.button('Multi-Player Options', multiPlayerOptionsButton)
        optionsMBut.add_self_to_kwargs()
        
        while True:
            optionsMenu.fill((202, 228, 241))
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
                        mixer.init()
                        mixer.music.load('Sounds/mainmenu.mp3')
                        mixer.music.set_volume(self.volume/100)
                        mixer.music.play(-1)
                        return
            pygame.display.update()
            self.mainClock.tick(self.FPS)
    
    def singlePlayerOptions(self, screen):
       optionsMenu = screen
       menuTheme = pygame_menu.themes.Theme(
           background_color=(202, 228, 241),
           title_background_color=(0, 0, 0, 0),
       )

       menu = pygame_menu.Menu(
           title="",
           height=self.screenHeight,
           width=self.screenWidth,
           theme=menuTheme)
       
       livesOn = int(self.gamemode) & 0x01
       timeOn = (int(self.gamemode) & 0x02) >> 1
       
       def setLivesOption(isLives, **kwargs):
           if(isLives):
               self.gamemode |= 0x1
           else:
               self.gamemode &= 0xE
           self.saveSettingToFile('SavedVariables.txt', 'gamemode', str(self.gamemode))
           print(livesOn, " ", timeOn, " ", self.gamemode)


       def setTimeOption(isTime, **kwargs):
           if(isTime):
               self.gamemode |= 0x2
           else:
               self.gamemode &= 0xD
           self.saveSettingToFile('SavedVariables.txt', 'gamemode', str(self.gamemode))
           print(livesOn, " ", timeOn, " ", self.gamemode)
       livesSwitch = menu.add.toggle_switch("Lives", onchange=setLivesOption, default=livesOn)
       timeSwitch = menu.add.toggle_switch("Timer", onchange=setTimeOption, default=timeOn)

       def setDifficulty(difficulty, difficultyIndex, **kwargs):
           value_tuple, index = difficulty
           self.difficulty = value_tuple[1]
           self.saveSettingToFile("SavedVariables.txt", "difficulty", str(value_tuple[1]))

       allDifficulties = [('Easy', 0),
                         ('Medium', 1),
                         ('Hard', 2)]
       difficultySelector = menu.add.dropselect(
           title="Difficulty",
           items=allDifficulties,
           # placeholder=allThemes[defaultCardTheme][0],
           onchange=setDifficulty,
           scrollbar_thick=5,
           selection_option_font=self.lifeFont,
           # selection_box_border_color=(0,0,0,0),
           selection_box_width=250,
           selection_box_height=250,
           placeholder= allDifficulties[self.difficulty][0],
           placeholder_add_to_selection_box=False
       )
       
       livesSwitch.add_self_to_kwargs()
       timeSwitch.add_self_to_kwargs()
       difficultySelector.add_self_to_kwargs()  # Callbacks will receive widget as parameter
       
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
                       mixer.init()
                       mixer.music.load('Sounds/mainmenu.mp3')
                       mixer.music.set_volume(self.volume/100)
                       mixer.music.play(-1)
                       return
           pygame.display.update()
           self.mainClock.tick(self.FPS)
    
    def multiplayerOptions(self, screen):
        optionsMenu = screen
        menuTheme = pygame_menu.themes.Theme(
            background_color=(202, 228, 241),
            title_background_color=(0, 0, 0, 0),
        )

        menu = pygame_menu.Menu(
            title="",
            height=self.screenHeight,
            width=self.screenWidth/2,
            theme=menuTheme)
        
        #reveals the number of teams based off the number of teams chosen
        def setTeamsOption(teamCountStr, teamCnt, **kwargs):
            self.teamCount = teamCnt
            print(self.teamCount)
            if(teamCnt <= 1):
                errorPlayerCountLable.hide()
                for team in range(maxTeamsEver):
                    teamPlayerCountSelectors[team].hide()
                return
            for team in range(teamCnt):
                teamPlayerCountSelectors[team].show()
            for team in range(maxTeamsEver - teamCnt):
                teamPlayerCountSelectors[-1 * (team - maxTeamsEver) - 1].hide()
            if(teamCnt > 1):
                checkPlayerCountPerTeamOptions(None, None)
        
        #sets the number of total players
        def setPlayerCountOptions(playerCountStr, playerCnt, **kwargs):
            #print(teamCount)
            teamCountList.clear()
            for players in range(playerCnt):
                stringPC = str(players)
                intPC = players
                teamCountList.append((stringPC, intPC))
            #print(playerCnt <= self.teamCount)
            if playerCnt <= self.teamCount:
                #print(playerCnt)
                teamSelector.set_value(str(playerCnt-1))
                setTeamsOption(None, playerCnt-1)
            teamSelector.update_items(teamCountList)
            self.playerCount = playerCnt
            checkPlayerCountPerTeamOptions(None, None)
            
        #both sets the number of players per team and checks that they equal the number of total players
        def checkPlayerCountPerTeamOptions(playerCountStr, playerCnt, **kwargs):
            attemptedPlayerCnt = 0
            for team in teamPlayerCountSelectors:
                if int(team.get_id()) > self.teamCount - 1:
                    break
                #print(team.get_id())
                #print(team.get_value()[1] + 1)
                attemptedPlayerCnt += team.get_value()[1] + 1
                #print(attemptedPlayerCnt)
                #print(self.playerCount)
            if not errorPlayerCountLable.is_visible() and attemptedPlayerCnt != self.playerCount and self.teamCount >= 2:
                errorPlayerCountLable.show()
            elif errorPlayerCountLable.is_visible() and attemptedPlayerCnt == self.playerCount:
                errorPlayerCountLable.hide()
                
        #reveals the text box for the time for the intro sequence if the introSequenceSwitch is set to showing
        def setIntroSequence(isLives, **kwargs):
            pass
        
        maxTeamsEver = 7 #since there are only allowed 8 possible players (because I think it would be too many after that), then there are only 7 possible teams. Otherwise it is a free for all, or 0 teams
        
        #needed: ability to select saved game modes
        #There probably should be a way to delete modes too, but that would be hard
        
        introSequenceSwitch = menu.add.toggle_switch("Intro Sequence", onchange=setIntroSequence, default=False, align=pygame_menu.locals.ALIGN_LEFT)
        
        #needed: deck count selector: columns and rows; cannot go above 8 rows or 12 columns
        
        playerCountList = [("2", 2),("3", 3),("4", 4),("5", 5),("6", 6),("7", 7), ("8", 8)]
        playerCountSelector = menu.add.selector("Total Player Count", 
                                                items=playerCountList, 
                                                onchange=setPlayerCountOptions, 
                                                style=pygame_menu.widgets.SELECTOR_STYLE_FANCY, 
                                                align=pygame_menu.locals.ALIGN_LEFT
                                                )
        teamCountList = []
        for players in range(self.playerCount):
            stringPC = None
            stringPC = str(players)
            intPC = players
            teamCountList.append((stringPC, intPC))
        teamSelector = menu.add.selector("Teams", items=teamCountList, onchange=setTeamsOption, style=pygame_menu.widgets.SELECTOR_STYLE_FANCY, align=pygame_menu.locals.ALIGN_LEFT)
        teamPlayerCountList = [("1", 1),("2", 2),("3", 3),("4", 4),("5", 5),("6", 6),("7", 7)]
        teamPlayerCountSelectors = [] #the number of players per team
        for i in range(maxTeamsEver):
            teamName = "Team " + str(i + 1) + " size"
            teamCountSelector = menu.add.selector(
                 teamName, 
                 selector_id=str(i),
                 items=teamPlayerCountList, 
                 onchange=checkPlayerCountPerTeamOptions, 
                 style=pygame_menu.widgets.SELECTOR_STYLE_FANCY, 
                 align=pygame_menu.locals.ALIGN_RIGHT
             )
            teamPlayerCountSelectors.append(teamCountSelector)
        errorPlayerCountLable = menu.add.label("The Added Player Count of Individual Teams needs to match the Total Player Count", font_size=10, align=pygame_menu.locals.ALIGN_LEFT)
        
        introSequenceSwitch.add_self_to_kwargs()
        playerCountSelector.add_self_to_kwargs()
        teamSelector.add_self_to_kwargs()
        for team in range(maxTeamsEver):
            teamPlayerCountSelectors[team].add_self_to_kwargs()
        for team in range(maxTeamsEver - self.teamCount):
            #print(-1 * (teams - maxTeams) - 1) 
            teamPlayerCountSelectors[-1 * (team - maxTeamsEver) - 1].hide()
        errorPlayerCountLable.add_self_to_kwargs()
        errorPlayerCountLable.hide()
        
        #needed: time between turns text box
        
        #needed: lives switch
            #lives per team text box
            #or
            #lives per player
                
        #needed: go until deck is depleted and then determine score to select winner (potential for tie) or make new decks until lives are depleted and determine winner that way (no ties)
        
        
        #needed: save upon finish switch
            #ability to save settings to file as new game mode text
            
        #needed: finished button
        
        while True:
            optionsMenu.fill((202, 228, 241))
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
                        pygame.mixer.music.stop()
                        return
            pygame.display.update()
            self.mainClock.tick(self.FPS)
    
    def settingsOptions(self, screen):
        optionsMenu = screen

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

        allCardThemes = [('Tarot', 'Tarot'),
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


        def setResolution(newRes, resX, resY, **kwargs):
            global screen
            value_tuple, index = newRes
            self.screenWidth = resX
            self.screenHeight = resY
            screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)
            menu.resize(resX, resY)
            self.saveSettingToFile("SavedVariables.txt", "screenWidth", str(resX))
            self.saveSettingToFile("SavedVariables.txt", "screenHeight", str(resY))

        allResolutions = [('2560 x 1440', 2560, 1440),
                          ('1920 x 1200', 1920, 1200),
                          ('1920 x 1080', 1920, 1080),
                          ('1680 x 1050', 1680, 1050),
                          ('1440 x 900', 1440, 900),
                          ('1366 x 768', 1366, 768),
                          ('1280 x 800', 1280, 800),
                          ('1280 x 720', 1280, 720),
                          ('1024 x 768', 1024, 768)]
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
            self.saveSettingToFile("SavedVariables.txt", "FPS", value_tuple[0])

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
            self.saveSettingToFile("SavedVariables.txt", "volume", str(val))
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

        themeSelector.add_self_to_kwargs()  
        resolutionSelector.add_self_to_kwargs()  
        fpsSelector.add_self_to_kwargs()  
        volumeSlider.add_self_to_kwargs() 

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
                        mixer.init()
                        mixer.music.load('Sounds/mainmenu.mp3')
                        mixer.music.set_volume(self.volume/100)
                        mixer.music.play(-1)
                        return
            pygame.display.update()
            self.mainClock.tick(self.FPS)

    def main_menu(self):
        screen = pygame.display.set_mode((self.screenWidth, self.screenHeight), 0, 32)

        titleFont = pygame.font.Font("assets/font.ttf", 50)

        # Main Menu Music
        mixer.init()
        mixer.music.load('Sounds/mainmenu.mp3')
        mixer.music.set_volume(self.volume/100)
        mixer.music.play(-1)

        white = (255, 255, 255)
        black = (0, 0, 0)

        
        while True:       
            screen.fill((202, 228, 241))
            self.draw_text_center('Memory Matching', titleFont, white,  self.screenWidth / 2, self.screenHeight / 6, screen)
            self.draw_text_center('Game', titleFont, white,  self.screenWidth / 2, self.screenHeight / 4, screen)

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Start Game Button
            START_BUTTON = Button(image=pygame.image.load("Assets/ButtonBG.jpg"), pos=(self.screenWidth/2, self.screenHeight*3/8), 
                            text_input="Start Game", font=pygame.font.Font("assets/font.ttf", 25), base_color="#d7fcd4", hovering_color="White")

            # Options buttons
            OPTIONS_BUTTON = Button(image=pygame.image.load("Assets/ButtonBG.jpg"), pos=(self.screenWidth/2, self.screenHeight*5/8), 
                            text_input="Options", font=pygame.font.Font("assets/font.ttf", 25), base_color="#d7fcd4", hovering_color="White")

            # Quit Game Button
            QUIT_BUTTON = Button(image=pygame.image.load("Assets/ButtonBG.jpg"), pos=(self.screenWidth/2, self.screenHeight*7/8), 
                            text_input="Quit", font=pygame.font.Font("assets/font.ttf", 25), base_color="#d7fcd4", hovering_color="White")

            for button in [START_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mixer.init()
                        mixer.music.load('Sounds/mainmenu.mp3')
                        mixer.music.set_volume(self.volume/100)
                        mixer.music.play(-1)
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Button events when specific buttons are clicked
                    if START_BUTTON.checkForInput(MENU_MOUSE_POS):
                        mixer.init()
                        mixer.music.load('Sounds/loading.mp3')
                        mixer.music.set_volume(self.volume/100)
                        mixer.music.play()
                        screen.fill(black)
                        self.sOrMOptions(screen)

                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        mixer.init()
                        mixer.music.load('Sounds/settings.mp3')
                        mixer.music.set_volume(self.volume/100)
                        mixer.music.play(-1)
                        self.settingsOptions(screen)
                    
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            
            pygame.display.update()
            self.mainClock.tick(self.FPS)
            
    def centerDeckX(self, xSize, col, screenWidth, minBorder):
        deckX = xSize * col
        availableSpace = screenWidth - minBorder * 2
        toXCenter = availableSpace - deckX
        toXCenter /= 2
        return toXCenter
    
    def stopAllFor(self, seconds):
        global running
        startTime = time.perf_counter()
        timeSinceStart = 0
        while timeSinceStart <= seconds and running:
            timeSinceStart = time.perf_counter()
            timeSinceStart -= startTime
            time.sleep(0.05)
           
    def game(self, window):
        
        def parallelEscape():
            global running
            while True:
                if keyboard.is_pressed("Esc"):
                    #when exiting game this will play main menu sound in the select screen, not finished
                    mixer.init()
                    mixer.music.load('Sounds/mainmenu.mp3')
                    mixer.music.set_volume(self.volume/100)
                    mixer.music.play(-1)
                    running = False
                time.sleep(0.05)
        
                
        global running
        running = True
        
        es = threading.Thread(target=parallelEscape)
        es.start()
        window.fill(self.black)
        t = self.createTable()

        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        black = (0, 0, 0)

        minBorder = 70
        inBTween = 10
        scale = self.setCardScale(minBorder, t.x, t.y, inBTween)
        xDim = int(250 * scale)
        yDim = int(350 * scale)
        xSize = xDim + inBTween
        ySize = yDim + inBTween
        toXCenter = self.centerDeckX(xSize, t.x, self.screenWidth, minBorder)
        timeToFlip = int(3000 * scale)  # can't be too fast or frames don't register
        
        mixer.init()
        mixer.music.load('Sounds/'+str(self.selectedTheme)+'.mp3')
        mixer.music.set_volume(self.volume/100)
        mixer.music.play(-1)
        
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
        
        self.stopAllFor(2)
        if(not running):
            pygame.event.clear()
            return False
        self.animate.flip(tempTable, timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, False)
        
        if self.difficulty == 0:
            matchTime = 30
        elif self.difficulty == 1:
            matchTime = 60
        else:
            matchTime = 45


        timer = matchTime
        sTime = time.time()

        timeLeft = int(timer - (time.time() - sTime))

        streak = 0

        quitG = False
        
        while running:
            self.mainClock.tick(self.FPS)
            mouse = pygame.mouse.get_pos()

            window.fill(black, (0, 0, 400, 40))  # so cards show during lose screen
            if self.gamemode == 1:
                self.draw_text("Lives: " + str(t.lives), self.lifeFont, white, 5, 0, window)
            elif self.gamemode == 2:
                self.draw_text("Time: " + str(timeLeft) + "s", self.lifeFont, white, 5, 0, window)
            elif self.gamemode == 3:
                self.draw_text("Lives: " + str(t.lives), self.lifeFont, white, 5, 0, window)
                self.draw_text("Time: " + str(timeLeft) + "s", self.lifeFont, white, 5, 20, window)

            self.draw_text("Score: " + str(t.score), self.lifeFont, white, 105, 0, window)

            if t.checkWin():
                window.fill(black, (0, 0, 400, 40))

                if len(t.selection) >= 2:
                    t.score = t.score + 100 + (50 * streak)
                    
                if self.gamemode == 1:
                    t.score = t.score + (t.lives * 100)
                    self.draw_text("Lives: " + str(t.lives), self.lifeFont, white, 5, 0, window)
                elif self.gamemode == 2:
                    t.score = t.score + (timeLeft * 10)
                    self.draw_text("Time: " + str(timeLeft) + "s", self.lifeFont, white, 5, 0, window)    
                elif self.gamemode == 3:
                    t.score = t.score + (t.lives * 100) + (timeLeft * 10)
                    self.draw_text("Lives: " + str(t.lives), self.lifeFont, white, 5, 0, window)
                    self.draw_text("Time: " + str(timeLeft) + "s", self.lifeFont, white, 5, 20, window)

                
                self.draw_text("Score: " + str(t.score), self.lifeFont, white, 105, 0, window)

                self.draw_text_center("You win!", self.endFont, green, self.screenWidth / 2, self.screenHeight / 4, window)

                mixer.init()
                mixer.music.load('Sounds/winner.mp3')
                mixer.music.set_volume(self.volume/100)
                mixer.music.play()
                               
                running, quitG, playAgain = self.endScreen(window, t.score)

                if playAgain:
                    mixer.init()
                    mixer.music.load('Sounds/'+str(self.selectedTheme)+'.mp3')
                    mixer.music.set_volume(self.volume/100)
                    mixer.music.play(-1)
                    return Game.game(self, window)

            elif (t.lives == 0 or timeLeft <= 0):
                hiddenTable = []
                for card in tempTable:
                    if (not card.shown):
                        hiddenTable.append(card)

                self.animate.flip(hiddenTable, 1000, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, True)

                self.draw_text_center("You lose!", self.endFont, red, self.screenWidth / 2, self.screenHeight / 4, window)
                mixer.init()
                mixer.music.load('Sounds/gameover.mp3')
                mixer.music.set_volume(self.volume/100)
                mixer.music.play()

                running, quitG, playAgain = self.endScreen(window, t.score)

                if playAgain:
                    mixer.init()
                    mixer.music.load('Sounds/'+str(self.selectedTheme)+'.mp3')
                    mixer.music.set_volume(self.volume/100)
                    mixer.music.play(-1)
                    return Game.game(self, window)

            else:
                t.update()
                for i in range(t.x):
                    for j in range(t.y):
                        surface = t.table[j][i].image.convert()
                        surface = pygame.transform.smoothscale(surface, (xDim, yDim))
                        t.table[j][i].rect = surface.get_rect()
                        t.table[j][i].makeRect((minBorder + toXCenter) + xSize * i, minBorder + ySize * j)
                pygame.display.update()
                
                if self.gamemode == 2 or self.gamemode == 3:
                    timeLeft = int(timer - (time.time() - sTime))

                if len(t.selection) >= 1:
                    if t.checkBomb():
                        
                        self.stopAllFor(1)
                        for c in t.selection:
                            if not (c.ID == "BOMB"):
                                cards = []
                                cards.append(c)
                                self.animate.flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, False)
                        
                        t.selection.clear()
                        if self.gamemode == 1:
                            t.lives = t.lives - 1
                        elif self.gamemode == 2:
                            sTime = sTime - 10
                        elif self.gamemode == 3:
                            t.lives = t.lives - 1
                            sTime = sTime - 10
                            
                    if len(t.selection) >= 2:
                        isMatch = t.checkMatch()
                        if isMatch == 2:
                            self.stopAllFor(1)
                            if(running):
                                self.animate.flip(t.selection, timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, False)
                                t.selection.clear()
                                if self.gamemode == 1 or self.gamemode == 3:
                                    t.lives = t.lives - 1
                                streak = 0
                        else:
                            if isMatch == 1:
                                match = t.selection[1].ID if t.selection[1].ID != "JOKER" else t.selection[0].ID
                                t.selection.clear()
                                for r in t.table:
                                    for c in r:
                                        if c.ID == match and not c.shown:
                                            cards = []
                                            cards.append(c)
                                            self.animate.flip(cards, timeToFlip, xDim, yDim, minBorder, xSize, ySize, toXCenter, window, True)
                            t.selection.clear()
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
                    pygame.quit()
                    sys.exit()  
            
        es.join(0)
        return quitG
        
    def endScreen(self, window, score):
        retryButton = Button(pygame.image.load("Assets/ButtonBG.jpg"), (self.screenWidth/2, self.screenHeight/ 4 * 2), "Restart", self.buttonFont, "White", "#d7fcd4")
        scoresButton = Button(pygame.image.load("Assets/ButtonBG.jpg"), (self.screenWidth/2, (self.screenHeight / 4 * 2) + 110), "High scores", self.buttonFont, "White", "#d7fcd4")
        mmButton = Button(pygame.image.load("Assets/ButtonBG.jpg"), (self.screenWidth/2, (self.screenHeight / 4 * 2) + 220), "Return to main menu", self.buttonFont, "White", "#d7fcd4")
        
        Score.saveScore(str(score))

        while True:
            self.mainClock.tick(self.FPS)
            mouse = pygame.mouse.get_pos()
            
            retryButton.update(window)
            retryButton.changeColor(mouse)
            
            scoresButton.update(window)
            scoresButton.changeColor(mouse)
            
            mmButton.update(window)
            mmButton.changeColor(mouse)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return [False, True, False]  # [Running, quitgame, playagain]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mixer.init()
                        mixer.music.load('Sounds/loading.mp3')
                        mixer.music.set_volume(self.volume/100)
                        mixer.music.play()
                        return [False, False, False]
                    if event.key == pygame.K_r:
                        window.fill(self.black)  # so cards show during lose screen
                        return [False, False, True]
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retryButton.checkForInput(mouse):
                        window.fill(self.black)
                        return [False, False, True]
                    elif scoresButton.checkForInput(mouse):
                        self.showScores(window, str(score))
                    elif mmButton.checkForInput(mouse):
                        mixer.init()
                        mixer.music.load('Sounds/loading.mp3')
                        mixer.music.set_volume(self.volume/100)
                        mixer.music.play()
                        return [False, False, False]
                    
    def createTable(self):
        if self.difficulty == 0:
            return Table(4, 3, self.selectedTheme, 5, self.difficulty, self.FPS)
        elif self.difficulty == 1:
            return Table(5, 5, self.selectedTheme, 10, self.difficulty, self.FPS)
        else:
            return Table(5, 5, self.selectedTheme, 6, self.difficulty, self.FPS)
        
    def showScores(self, window, pScore):
        window.fill(self.black, (0, 40, self.screenWidth, self.screenHeight))
        
        self.draw_text_center("High scores", pygame.font.SysFont("Times New Roman", 40), self.white, self.screenWidth / 2, self.screenHeight / 10, window)
        
        scores = Score.readScores()
        textArea = ((self.screenHeight / 10) * 9) / 10
        pos = (self.screenHeight / 10) + 40
        
        for score in scores:
            if score == pScore:
                self.draw_text_center(score, self.buttonFont, self.green, self.screenWidth / 2, pos, window)
            else:
                self.draw_text_center(score, self.buttonFont, self.white, self.screenWidth / 2, pos, window)
                
            pos = pos + textArea
        
        while True:
            self.mainClock.tick(self.FPS)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
