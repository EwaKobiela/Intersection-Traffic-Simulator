import pygame
import os
from traffic_light import TrafficLight

CAR_L = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_left.png")), (150, 60))
CAR_R = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_right.png")), (150, 60))
CAR_U = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_up.png")), (60, 150))
CAR_D = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_down.png")), (60, 150))

class Car:
    def __init__(self, orientation):
        self.orientation = orientation
        self.car_img = None
        self.x = None
        self.y = None
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

    def move(self, vel, lights):
        if (self.orientation == "L"):
            if (self.x + self.car_img.get_width() == 250 and lights[0].state == "red"):
                self.x = self.x
            else:
                self.x += vel
        elif (self.orientation == "R"):
            if (self.x == 550 and lights[1].state == "red"):
                self.x = self.x
            else:
                self.x -= vel
        elif (self.orientation == "U"):
            if (self.y + self.car_img.get_height() == 180 and  lights[2].state == "red"):
                self.y = self.y
            else:
                self.y += vel
        elif (self.orientation == "D"):
            if (self.y == 450 and lights[3].state == "red"):
                self.y = self.y
            else:
                self.y -= vel
