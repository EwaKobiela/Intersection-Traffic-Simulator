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

class Car:
    def __init__(self, orientation):

        self.orientation = orientation

        if (self.orientation == "L"):
            self.car_img = CAR_L
            self.x = 10
            self.y = 365
        elif (self.orientation == "R"):
            self.car_img = CAR_R
            self.x = (800 - CAR_D.get_width() - 10)
            self.y = 365
        elif (self.orientation == "U"):
            self.car_img = CAR_U
            self.x = 450
            self.y = 10
        elif (self.orientation == "D"):
            self.car_img = CAR_D
            self.x = 450
            self.y = (630 - CAR_D.get_height() - 10)

    def draw(self, window):
        window.blit(self.car_img, (self.x, self.y))


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)

    prob_L = 30
    prob_R = 30
    prob_U = 20
    prob_D = 20

    def generate_car():
        my_list = ['L'] * prob_L + ['R'] * prob_R + ['U'] * prob_U + ['D'] * prob_D
        dir = random.choice(my_list)
        print(dir)
        car = Car(dir)
        car.draw(WIN)


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

        for i in range(0, 1):
            generate_car()

        pygame.display.update() #Refresh display


    while run:
        clock.tick(FPS)
        draw_window()



        #Triggering events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

main()