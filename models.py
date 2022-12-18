from utils import *
from constants import *

# a class that contains 
class GUI:
    def __init__(self):
        self.finished = False
        self.started = False

    def reset(self):
        self.started = False
        self.finished = False

    def finish(self): 
        self.finished = True

    def start(self):
        self.started = True
    
    def game_finished():
        return self.finished

# a class that represents all the objects 
class AbstractObject:
    # these are used to scale the meter system in the car coordinates to pixels 
    X_SCALING_VALUE = 3 * ZOOM
    Y_SCALING_VALUE = 3 * ZOOM
    def __init__(self, img, idd, dx, dy, objectType, vx, vy, ax, ay, prob10bstacle, timestamp):
        self.id = idd
        self.img = img
        self.dx = dx / 128 * self.X_SCALING_VALUE # converts dx to pixels 
        self.dy = dy / 128 * self.Y_SCALING_VALUE 
        self.objectType = objectType
        self.vx = vx 
        self.vy = vy
        self.ax = ax
        self.ay= ay
        self.prob10bstacle = prob10bstacle
        self.timestamp = float(timestamp)
        self.setImage()

    def __key(self):
        return (self.dx, self.dy, self.objectType, self.vx, self.vy, self.ax, self.ay, self.prob10bstacle)
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self, other):
        x1, y1 = self.getXYfromOriginInMeters()
        x2, y2 = other.getXYfromOriginInMeters()
        delta_x, delta_y = abs(x2 - x1), abs(y2 - y1)

        # checking if it's a truck or a car 
        # because a truck is much bigger than a car 
        # this way there's accuracy in deleting objects detected by several sensors
        if(self.objectType == 1 or other.objectType == 1): 
            return delta_x <= 7.5 and delta_y <= 4
        else:
            return delta_x <= 5.5 and delta_y <= 3

    def draw(self, win):
        return self.drawImage(win, self.img)

    # draws a certain image instead of the current one
    def drawImage(self, win, img):
        oldX, oldY = convertToPygame(win, self.dx, self.dy)
        currentX, currentY = adjustPositionToObject(img, oldX, oldY)
        win.blit(img, (currentX, currentY))
        return oldX, oldY
    
    # transforms the objects current position to meter system from origin (0,0) => The host car EGO
    def getXYfromOriginInMeters(self):
        return ((self.dx / self.X_SCALING_VALUE), (self.dy / self.Y_SCALING_VALUE))
    
    # chooses the object image according to the Object Type
    def setImage(self):
        if self.objectType == 2 or self.objectType == 6: 
            self.img = CAR
        elif self.objectType == 1:
            self.img = TRUCK
        elif self.objectType == 3 or self.objectType == 4:
            self.img = BIKE
        elif self.objectType == 5:
            self.img = PEDESTRIAN
        elif self.objectType == 7:
            self.img = EGO