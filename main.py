import pygame
import time
import math
from utils import *
from models import *
from constants import *
from csvReader import *
import cv2

pygame.font.init()

# Initial Constant used to initialize the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
ORIGIN_X, ORIGIN_Y = WIN.get_width()/2, WIN.get_height()/2
pygame.display.set_caption("Automotive stimulation!!")
MAIN_FONT = pygame.font.SysFont("comicsans", 24)
SECOND_FONT = pygame.font.SysFont("comicsans", 12)
HOST_CAR_OBJECT = AbstractObject(EGO, -1, 0, 0,7,-1,-1,-1,-1,-1,-1)

images = [(BLUE_BACKGROUND, (0, 0)), (EGO, (200, 85*ZOOM/2)), (CAR, (200, 120*ZOOM/2)), (TRUCK, (200, 155*ZOOM/2)), (BIKE, (200, 185*ZOOM/2)), (PEDESTRIAN, (200, 220*ZOOM/2)), (UNKNOWN, (200, 255*ZOOM/2)), (BLIND, (200, 285*ZOOM/2))]
gui = GUI()

# blind spot
BLIND_LEFT_REC_POINT = convertMeterPointToPygame(WIN, 0.85 - 1, 1.55, ZOOM)
BLIND_RIGHT_REC_POINT = convertMeterPointToPygame(WIN, 0.85 - 1, -1.55, ZOOM)
REC_WIDTH_PIXELS = convertMetersToPixels(10, ZOOM)
REC_HEIGHT_PIXELS = convertMetersToPixels(2.3, ZOOM)
BLIND_RECT_LEFT = pygame.Rect(BLIND_LEFT_REC_POINT[0] - REC_WIDTH_PIXELS/2, BLIND_LEFT_REC_POINT[1] - REC_HEIGHT_PIXELS/2, REC_WIDTH_PIXELS, REC_HEIGHT_PIXELS)
BLIND_RECT_RIGHT = pygame.Rect(BLIND_RIGHT_REC_POINT[0] - REC_WIDTH_PIXELS/2, BLIND_RIGHT_REC_POINT[1] - REC_HEIGHT_PIXELS/2, REC_WIDTH_PIXELS, REC_HEIGHT_PIXELS)


# controlling FPS 
clock = pygame.time.Clock()
FPS = 25

# Video related
VIDEO = cv2.VideoCapture('data/video.avi')
success, video_image = VIDEO.read()

FRAME_COUNTER_MAX = 1
video_frame_counter = FRAME_COUNTER_MAX
current_video_surf = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (400, 300))

def drawVideoSurf(win, video_surf):
    win.blit(video_surf, (940, 30))

def drawVideo(win, video):
    global current_video_surf
    success, video_image = video.read()
    if success:
        video_surf = pygame.transform.scale(pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR"), (400, 300))
        current_video_surf = video_surf
        drawVideoSurf(win, video_surf)

def updateVideoFrame():
    global video_frame_counter
    if (video_frame_counter >= FRAME_COUNTER_MAX):
        drawVideo(WIN, VIDEO)
        video_frame_counter = 0
    else:
        drawVideoSurf(WIN, current_video_surf)
        # the higher, the faster the video
        video_frame_counter += 0.2

# a function used to draw images and objects arrays to the window 
# it also resets the window with the background and updates the video frame
def draw(win, images, objects):
    for img, pos in images:
        win.blit(img, pos)

    pygame.draw.rect(WIN, (115, 143, 157), BLIND_RECT_LEFT)
    pygame.draw.rect(WIN, (115, 143, 157), BLIND_RECT_RIGHT)

    printText(WIN,"Timestamp: ", MAIN_FONT, pos=(50,50*ZOOM/2))
    printText(WIN,"Ego: ", MAIN_FONT, pos=(50,85*ZOOM/2))
    printText(WIN,"Car: ", MAIN_FONT, pos=(50,120*ZOOM/2))
    printText(WIN,"Truck: ", MAIN_FONT, pos=(50,155*ZOOM/2))
    printText(WIN,"Bike: ", MAIN_FONT, pos=(50,185*ZOOM/2))
    printText(WIN,"Pedestrian: ", MAIN_FONT, pos=(50,220*ZOOM/2))
    printText(WIN,"UNKNOWN: ", MAIN_FONT, pos=(50,255*ZOOM/2))
    printText(WIN,"BLIND: ", MAIN_FONT, pos=(50,285*ZOOM/2))

    pygame.draw.line(win, (200,0,0),(300,WIN.get_height()/2),(1066, WIN.get_height()/2))
    pygame.draw.line(win, (200,0,0),(WIN.get_width()/2,0),(WIN.get_width()/2, WIN.get_height()))

    for obj in objects:
        cX, cY = obj.draw(win)
        printText(WIN, str(obj.getXYfromOriginInMeters()),SECOND_FONT, (0,200,0), (cX, cY))

    updateVideoFrame()
    pygame.display.update()

# this function checks if the current obj is in blind spot
def isInBlindSpot(win,obj, rec):
    oldX, oldY = convertToPygame(win, obj.dx, obj.dy)
    currentX, currentY = adjustPositionToObject(obj.img, oldX, oldY)
    obj_rect = obj.img.get_rect(topleft = (currentX, currentY))
    if rec.colliderect(obj_rect):
        printText(WIN,"Something is in the BLIND SPOT", MAIN_FONT, color = "red", pos=(50,650))
        return True;
    return False

def drawObjects(objs):
    cX, cY = 0,0
    for obj in objs:
        if (obj.dx == 0 and obj.dy == 0):
            continue
        isBlind = (isInBlindSpot(WIN, obj, BLIND_RECT_LEFT) or isInBlindSpot(WIN, obj, BLIND_RECT_RIGHT))
        if isBlind:
            cX, cY = obj.drawImage(WIN, img = BLIND)
        else:
            cX, cY = obj.draw(WIN)
        printText(WIN, str(obj.getXYfromOriginInMeters()),SECOND_FONT, (0,200,0), (cX, cY))

def getObjectsFromAllSensors(timestamp):
    # holds the current objects detected by all sensors
    objs = []
    for obj in camera_objects[timestamp]:
        objs.append(obj)
    for obj in corner0_objects[timestamp]:
        objs.append(obj)
    for obj in corner1_objects[timestamp]:
        objs.append(obj)
    for obj in corner2_objects[timestamp]:
        objs.append(obj)
    for obj in corner3_objects[timestamp]:
        objs.append(obj)

    # removing duplicate objects 
    objs.sort(key=lambda x: x.getXYfromOriginInMeters())

    unique_objs = []
    for obj in objs:
        if obj not in unique_objs:
            unique_objs.append(obj)
    return unique_objs

draw(WIN, images, [])
blit_text_center(
    WIN, MAIN_FONT, f"Start Simulation")
pygame.display.update()

while not gui.started:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

        if event.type == pygame.KEYDOWN:
            gui.start()

skip = False
paused = False
i = 0
# it doesn't matter what array we use cuz they have the same keys anyway
timestamp_list = list(corner0_objects.keys())

# this list is used for prediction
prediction_list = []

while i < len(corner0_objects):
    timestamp = timestamp_list[i]
    # checking if you're closing the app
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            gui.finish()
            exit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused 
    # implementing pause control
    if not paused:
        if (skip == True):
            skip = False
            continue
        skip = True
        # controlling the FPS
        clock.tick(FPS)

        unique_objs = getObjectsFromAllSensors(timestamp)
        # prediction
        # get common objs
        common_objs = [obj for obj in prediction_list if obj in unique_objs]
        # get uncommon objs
        uncommon_objs = [obj for obj in prediction_list if obj not in unique_objs]
        # add unique_objs to uncommon objs
        uncommon_objs.extend(unique_objs)
        prediction_list = uncommon_objs

        # this draws all the objects in the current frame
        drawObjects(unique_objs)

        if (i != len(corner0_objects) - 1):
        # predict the next values
            for obj in prediction_list:
                # predicts the next dx and dy for obj using vx and vy 
                next_timestamp = timestamp_list[i+1]
                obj2 = next((x for x in getObjectsFromAllSensors(next_timestamp) if x.id == obj.id), None)
                if(obj2 is None): 
                    continue
                obj.dx, obj.dy = predict(obj, obj2)
                obj.dx /= 128
                obj.dy /= 128

        # updating timestamp in the window surface
        printText(WIN,"Timestamp: " + timestamp, MAIN_FONT, pos=(50,50*ZOOM/2))
        pygame.display.update()

        # reseting the screen, by drawing the background and Ego 
        draw(WIN, images, [HOST_CAR_OBJECT])
        
        i += 1
    else:
        blit_text_center(
            WIN, MAIN_FONT, f"Start Simulation")
        pygame.display.update()

pygame.quit()

# ! Prediction
# ! for each timestamp:
    # * get current objects 
    # * remove duplicate objects 
    # * add them to the prediction list
    # * predict their next values

    # ? get current objects
    # ? remove duplicate objects
    # ? Are the predicted objects there in the current ones> 
        # ! if there aren't:
            # * check if they are too far
            # * or they are in the blind spot:
                # * if they are, keep the uncommon ones in the predicted list 
                # * then change them to 
                        # ! RED
        # ! if there are:
            # * remove the common ones from the predicted list 
            # * add the unique list
    # ? draw the predicted list
    # ? predict the next values
    # ? repeat
