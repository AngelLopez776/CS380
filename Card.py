import pygame

class Card():
    def __init__(self, theme, ID):
        super().__init__()
        
        self.ID = ID
        self.col = 0
        self.row = 0
        
        folder = "theme_" + str(theme) + "/"
        img = str(ID) + ".jpg"
        
        path = ("images/" + folder + img)
        
        self.front_image = pygame.image.load(path)
        #self.front_image = pygame.transform.smoothscale(self.front_image, (int(self.front_image.get_width() / 2), int(self.front_image.get_height() / 2)))
        self.back_image = pygame.image.load("images/" + folder + "card_back.jpg")
        #self.back_image = pygame.transform.scale(self.back_image, (int(self.back_image.get_width() / 2), int(self.back_image.get_height() / 2)))
        
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