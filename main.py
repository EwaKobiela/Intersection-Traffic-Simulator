import pygame
import os
import random
import cv2 as cv
from wincapture import get_screenshot
import numpy as np
from vision import Vision
from car import Car
from traffic_light import TrafficLight
import time
pygame.font.init()

#############################################################################################################
##  Intersection Traffic Simulator
##  by Ewa Kobiela & Jan Laskowski
#############################################################################################################

#Initialize window
pygame.font.init()
WIDTH, HEIGHT = 800, 630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intersection traffic simulator")

#Load images
BG = pygame.image.load(os.path.join("assets", "intersection.jpg"))

#Load trained model (OpenCV classifier)
cascade = cv.CascadeClassifier('cascade/cascade.xml')
#Load vision class
vision = Vision(None)
#wincap = WindowCapture('')

#Define/generate probabilities
prob_L = 25
prob_R = 25
prob_U = 25
prob_D = 25

class Road:
    def __init__(self, orientation, state):
        self.state = state
        self.orientation = orientation

    def change_lights(self, state):
        if (state == "red"):
            self.state = "red"
        elif (state == "green"):
            self.state = "green"


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    vel = 1 #Cars' velocity
    cars = []
    #     = [left, right, up, down]
    queue = [False, False, False, False]
    car_at_crossroad = False
    history = []
    count = 400
    light_left = TrafficLight("L")
    light_right = TrafficLight("R")
    light_up = TrafficLight("U")
    light_down = TrafficLight("D")
    lights = [light_left, light_right, light_up, light_down]

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
                    R += 1
                elif history[i] == "U":
                    U += 1
                elif history[i] == "D":
                    D += 1
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
        #true_probL_label = main_font.render(f"Prob L: {prob_L*0.01}", 1, (0, 0, 0))
        #true_probR_label = main_font.render(f"Prob R: {prob_R*0.01}", 1, (0, 0, 0))
        #true_probU_label = main_font.render(f"Prob U: {prob_U*0.01}", 1, (0, 0, 0))
        #true_probD_label = main_font.render(f"Prob D: {prob_D*0.01}", 1, (0, 0, 0))

        true_probL_label = main_font.render(f"Intersection", 1, (0, 0, 0))
        true_probR_label = main_font.render(f"Traffic", 1, (0, 0, 0))
        true_probU_label = main_font.render(f"Simulator", 1, (0, 0, 0))
        true_probD_label = main_font.render(f"Ewa Kobiela & Jan Laskowski", 1, (0, 0, 0))

        WIN.blit(true_probL_label, (10, 10))
        WIN.blit(true_probR_label, (10, true_probR_label.get_height() + 20))
        WIN.blit(true_probU_label, (10, true_probU_label.get_height() * 2 + 30))
        WIN.blit(true_probD_label, (7, true_probD_label.get_height() * 3 + 40))

        L, R, U, D = calc_probab()
        calc_probL_label = main_font.render(f"Prob L: {round(L, 2)}", 1, (0, 0, 0))
        calc_probR_label = main_font.render(f"Prob R: {round(R, 2)}", 1, (0, 0, 0))
        calc_probU_label = main_font.render(f"Prob U: {round(U, 2)}", 1, (0, 0, 0))
        calc_probD_label = main_font.render(f"Prob D: {round(D, 2)}", 1, (0, 0, 0))

        WIN.blit(calc_probL_label, (WIDTH - calc_probL_label.get_width() - 10, 10))
        WIN.blit(calc_probR_label, (WIDTH - calc_probR_label.get_width() - 10, true_probR_label.get_height() + 20))
        WIN.blit(calc_probU_label, (WIDTH - calc_probU_label.get_width() - 10, true_probU_label.get_height() * 2 + 30))
        WIN.blit(calc_probD_label, (WIDTH - calc_probD_label.get_width() - 10, true_probD_label.get_height() * 3 + 40))


        for car in cars:
            car.draw(WIN)

        #Draw lights
        light_left.draw(WIN)
        light_right.draw(WIN)
        light_up.draw(WIN)
        light_down.draw(WIN)

        pygame.display.update() #Refresh display

    def detect(rectangles):
        for rect in rectangles:
            # Detect cars in the middle of the crosroad
            if (rect[1] > 180 and rect[1] < 450 and rect[0] > 250 and rect[0] < 550 and rect[2] < 100):
                car_at_crossroad = True
            else:
                car_at_crossroad = False
            # If car detected in the middle nobody else can go
            if (car_at_crossroad == True):
                for light in lights:
                    light.change_to_red()

            # Detect queing cars
            if (rect[1] > 325 and rect[1] < 450 and rect[0] < 250 and rect[2] < 100):
                queue[0] = True
            if (rect[1] > 200 and rect[1] < 325 and rect[0] > 550 and rect[2] < 200):
                queue[1] = True
            if (rect[0] > 280 and rect[0] < 400 and rect[1] < 180 and rect[2] < 100):
                queue[2] = True
            if (rect[0] > 400 and rect[0] < 600 and rect[1] > 450 and rect[2] < 100):
                queue[3] = True

    def manage_queue(queue, lights):
        if (queue[0] == True):
            lights[0].change_to_green()
            lights[1].change_to_red()
            lights[2].change_to_red()
            lights[3].change_to_red()
            queue[0] = False
        if (queue[1] == True):
            lights[0].change_to_red()
            lights[1].change_to_green()
            lights[2].change_to_red()
            lights[3].change_to_red()
            queue[1] = False
        if (queue[2] == True):
            lights[0].change_to_red()
            lights[1].change_to_red()
            lights[2].change_to_green()
            lights[3].change_to_red()
            queue[2] = False
        if (queue[3] == True):
            lights[0].change_to_red()
            lights[1].change_to_red()
            lights[2].change_to_red()
            lights[3].change_to_green()
            queue[3] = False

    while run:
        clock.tick(FPS)
        count += 1
        draw_window()
        screenshot = get_screenshot()
        screenshot = np.array(screenshot)

        #Detect cars
        rectangles = cascade.detectMultiScale(screenshot)
        detection_image = vision.draw_rectangles(screenshot, rectangles)

        detect(rectangles)
        if (queue):
            manage_queue(queue, lights)
        #else:
            #change to mose probable one

        # Draw detection results in the image
        cv.imshow("x", detection_image)

        #In case of closing window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #Generate new car after 400 frames
        if (count >= 400):
            prob = ["L"]*prob_L + ["R"]*prob_R + ["U"]*prob_U + ["D"]*prob_D
            x = random.choice(prob)
            car = Car(x)
            cars.append(car)
            history.append(x)
            count = 0

        #Move cars
        for car in cars[:]:
            car.move(vel, lights)
            if (car.x > 800 or car.y > 630 or car.x <= 0 or car.y <= 0):
                cars.remove(car)

main()
