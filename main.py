import pygame
import os
import random
import time
pygame.font.init()

#Initialize window
pygame.font.init()
WIDTH, HEIGHT = 800, 630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intersection traffic simulator")

#Load images
CAR_L = pygame.image.load(os.path.join("assets", "car_left.jpg"))
CAR_R = pygame.image.load(os.path.join("assets", "car_right.jpg"))
CAR_U = pygame.image.load(os.path.join("assets", "car_up.jpg"))
CAR_D = pygame.image.load(os.path.join("assets", "car_down.jpg"))
BG = pygame.image.load(os.path.join("assets", "intersection.jpg"))

#Define/generate probabilities
prob_L = 30
prob_R = 30
prob_U = 20
prob_D = 20

class Car:
    CARS_MAP = {
        "L": (CAR_L),
        "R": (CAR_R),
        "U": (CAR_U),
        "D": (CAR_D),
    }
    def __init__(self, orientation):
        self.orientation = orientation
        self.car_img = self.CARS_MAP[orientation]
        if (self.orientation == "L"):
            self.x = 10
            self.y = 345
        elif (self.orientation == "R"):
            self.x = (800 - CAR_D.get_width() - 10)
            self.y = 345
        elif (self.orientation == "U"):
            self.x = 450
            self.y = 10
        elif (self.orientation == "D"):
            self.x = 450
            self.y = (630 - CAR_D.get_height() - 10)

    def draw(self, window):
        window.blit(self.car_img, (self.x, self.y))

    def move(self, vel):
        self.x += vel

#class Car_L(Car):


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    vel = 1 #Cars' velocity
    cars = []
    history = []
    count = 400

    def calc_probab():
        L= 0
        R = 0
        U = 0
        D = 0
        if len(history) > 0:
            for i in range(len(history)):
                if history[i] == "L":
                    L += 1
                elif history[i] == "R":
                    R += R
                elif history[i] == "U":
                    U += U
                elif history[i] == "D":
                    D += D
            if (L==0):
                L=0
            else:
                L = L / len(history)
            if (R==0):
                R=0
            else:
                R = R / len(history)
            if (U==0):
                U=0
            else:
                U = U / len(history)
            if (D==0):
                D=0
            else:
                D = D / len(history)
        return L, R, U, D


    def draw_window():
        WIN.blit(BG, (0, 0))    #Draw background
        #draw text
        true_probL_label = main_font.render(f"Prob L: {prob_L}", 1, (0, 0, 0))
        true_probR_label = main_font.render(f"Prob R: {prob_R}", 1, (0, 0, 0))
        true_probU_label = main_font.render(f"Prob U: {prob_U}", 1, (0, 0, 0))
        true_probD_label = main_font.render(f"Prob D: {prob_D}", 1, (0, 0, 0))
        #calc_val_label

        WIN.blit(true_probL_label, (10, 10))
        WIN.blit(true_probR_label, (10, true_probR_label.get_height() + 20))
        WIN.blit(true_probU_label, (10, true_probU_label.get_height() * 2 + 30))
        WIN.blit(true_probD_label, (10, true_probD_label.get_height() * 3 + 40))
        #WIN.blit(true_val_label, (WIDTH - level_label.get_widht() - 10, 10))

        L, R, U, D = calc_probab()
        calc_probL_label = main_font.render(f"Prob L: {L}", 1, (0, 0, 0))
        calc_probR_label = main_font.render(f"Prob R: {R}", 1, (0, 0, 0))
        calc_probU_label = main_font.render(f"Prob U: {U}", 1, (0, 0, 0))
        calc_probD_label = main_font.render(f"Prob D: {D}", 1, (0, 0, 0))

        WIN.blit(calc_probL_label, (WIDTH - calc_probL_label.get_width() - 10, 10))
        WIN.blit(calc_probR_label, (WIDTH - calc_probR_label.get_width() - 10, true_probR_label.get_height() + 20))
        WIN.blit(calc_probU_label, (WIDTH - calc_probU_label.get_width() - 10, true_probU_label.get_height() * 2 + 30))
        WIN.blit(calc_probD_label, (WIDTH - calc_probD_label.get_width() - 10, true_probD_label.get_height() * 3 + 40))


        for car in cars:
            car.draw(WIN)

        pygame.display.update() #Refresh display


    while run:
        clock.tick(FPS)
        clock
        draw_window()

        #Triggering events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if (count == 400):
            # to delete
            car = Car("L")
            cars.append(car)
            history.append("L")
            count = 0

        for car in cars[:]:
            car.move(vel)
            count += 1

main()
