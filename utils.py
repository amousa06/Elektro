import csv
import pygame

# scales images with a factor
def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


# a utility function to rotate a surface around its center
def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

# a utility function to draw a text with the given font, color, position
def printText(win, text, font, color = (200,200,200), pos = (100,100)):
    render = font.render(text, 1, color)
    win.blit(render, pos)

# draw a text in the center point
def blit_text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    blit_center(win, render)

# render in the center point
def blit_center(win, render):
    win.blit(render, (win.get_width()/2 - render.get_width() / 2, win.get_height()/2 - render.get_height()/2))

# convert coordinate to Pygame axis
def convertToPygame(win, x, y): 
    return (win.get_width() / 2 - y, win.get_height() / 2 - x)

# convert meters to pixels while also considering how much the content is zoomed
def convertMetersToPixels(m, zoom):
    return m * 3 * zoom

# pygame uses top left point of surfaces to position the objects
# this function makes it use center point instead 
def adjustPositionToObject(obj, x, y): 
    return ((x - obj.get_width() / 2), (y - obj.get_height() / 2))

# converts meter points in the car coordinates to pygame window coordinates
def convertMeterPointToPygame(win, x, y, zoom):
    # 1 m = 1 * 3 * ZOOM
    pX = convertMetersToPixels(x,zoom)
    pY = convertMetersToPixels(y,zoom)

    return convertToPygame(win, pX, pY)

def dXpredict(obj1, obj2):
    return obj1.dx + ((obj2.timestamp-obj1.timestamp)*(obj1.vx)) - (0.5*obj1.ax*(obj2.timestamp-obj1.timestamp)*(obj2.timestamp-obj1.timestamp))

def dYpredict(obj1, obj2):
    return obj1.dy + ((obj2.timestamp-obj1.timestamp)*(obj1.vy)) - (0.5*obj1.ay*(obj2.timestamp-obj1.timestamp)*(obj2.timestamp-obj1.timestamp))
# this function predicts the dx and dy of the next obj using obj1 and obj2
def predict(obj1, obj2):
    return (dXpredict(obj1, obj2), dYpredict(obj1, obj2))

# ! Camera: 
    # * for each time stamp and for each object ID: 
        # ? object timestamp
        # ? object dx 
        # ? object dy 
        # ? object vx 
        # ? object vy
        # ? object type

# ! Corner Radars
    # * for each time stamp and for each object ID: 
        # ? object timestamp
        # ? object ax 
        # ? object ay
        # ? object dx
        # ? object dy
        # ? object dz
        # ? probObstacle 
        # ? object vx
        # ? object vy

# ! Camera Position 
    # ? posXCam
    # ? posYCam
    # ? posZCam