from utils import *
import cv2

# if you want to see everything, set it to 1, however, everything will be very small
# for a nice zoomed view set it to 4
ZOOM = 4
CAR = scale_image(pygame.image.load("imgs/car_400.png"), ZOOM/4)
CAR_DIMENSIONS = (4, 2) # in meters 
TRUCK = scale_image(pygame.image.load("imgs/truck_400.png"), ZOOM/4)
TRUCK_DIMENSIONS = (6, 3) # in meters
BLUE_BACKGROUND = pygame.image.load("imgs/blue_background.png")
UNKNOWN = scale_image(pygame.image.load("imgs/unknown_400.png"), ZOOM/4)
PEDESTRIAN = scale_image(pygame.image.load("imgs/pedestrian_400.png"), ZOOM/4)
BIKE = scale_image(pygame.image.load("imgs/bike_400.png"), ZOOM/4)
EGO = scale_image(pygame.image.load("imgs/ego_400.png"), ZOOM/4)
BLIND = scale_image(pygame.image.load("imgs/blind_400.png"), ZOOM/4)

WIDTH, HEIGHT = BLUE_BACKGROUND.get_width(), BLUE_BACKGROUND.get_height()