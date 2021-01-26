import pygame
import os

CAR_L = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_left.png")), (150, 60))
CAR_R = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_right.png")), (150, 60))
CAR_U = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_up.png")), (60, 150))
CAR_D = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_down.png")), (60, 150))

class Car:
    def __init__(self, orientation):
        self.orientation = orientation
        if (self.orientation == "L"):
            self.x = 10
            self.y = 345
            self.car_img = CAR_L
        elif (self.orientation == "R"):
            self.x = (800 - CAR_D.get_width() - 10)
            self.y = 240
            self.car_img = CAR_R
        elif (self.orientation == "U"):
            self.x = 320
            self.y = 10
            self.car_img = CAR_U
        elif (self.orientation == "D"):
            self.x = 430
            self.y = (630 - CAR_D.get_height() - 10)
            self.car_img = CAR_D


    def draw(self, window):
        window.blit(self.car_img, (self.x, self.y))

    def move(self, vel):
        #print("Car position: ", car.x)
        # Left - x = 115
        if (self.orientation == "L"):
            #if
            self.x += vel
        elif (self.orientation == "R"):
            self.x -= vel
        elif (self.orientation == "U"):
            self.y += vel
        elif (self.orientation == "D"):
            self.y -= vel
