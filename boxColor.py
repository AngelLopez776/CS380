class BoxColor:
    def __init__(self):
        self.boxColor = (0,0,0)
        self.x = 0;
        self.y = 0;
        self.z = 0;
    
    def setCol(self, x, y, z):
        self.boxColor = (x, y, z)
        self.x = x
        self.y = y
        self.z = z
        
    def getCol(self):
        return (self.x, self.y, self.z)