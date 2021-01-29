import pygame
import os

RED = pygame.transform.scale(pygame.image.load(os.path.join("assets", "red_light.png")), (60, 45))
GREEN = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green_light.png")), (60, 45))

class TrafficLight:
    def __init__(self, position):
        self.position = position
        self.state = None
        self.x = None
        self.y = None
        if (self.position == "L"):
            self.x = 200
            self.y = 420
        if (self.position == "R"):
            self.x = 520
            self.y = 180
        if (self.position == "U"):
            self.x = 240
            self.y = 140
        if (self.position == "D"):
            self.x = 500
            self.y = 460
        #by default all lights are red
        self.img = RED

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def change_to_green(self):
        self.img = GREEN
        self.state = "green"

    def change_to_red(self):
        self.img = RED
        self.state = "red"