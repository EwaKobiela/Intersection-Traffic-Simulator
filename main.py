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
CAR_L = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_left.png")), (150, 60))
CAR_R = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_right.png")), (150, 60))
CAR_U = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_up.png")), (60, 150))
CAR_D = pygame.transform.scale(pygame.image.load(os.path.join("assets", "car_down.png")), (60, 150))
BG = pygame.image.load(os.path.join("assets", "intersection.jpg"))

#Define/generate probabilities
prob_L = 50
prob_R = 20
prob_U = 25
prob_D = 5

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
        if (self.orientation == "L"):
            self.x += vel
        elif (self.orientation == "R"):
            self.x -= vel
        elif (self.orientation == "U"):
            self.y += vel
        elif (self.orientation == "D"):
            self.y -= vel

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
                    R += 1
                elif history[i] == "U":
                    U += 1
                elif history[i] == "D":
                    D += 1
                print("i=", i)
            #print(history)
            print("Orginal L: ", L, "R: ", R, "U: ", U, "D: ", D, "len: ", len(history))
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
        true_probL_label = main_font.render(f"Prob L: {prob_L*0.01}", 1, (0, 0, 0))
        true_probR_label = main_font.render(f"Prob R: {prob_R*0.01}", 1, (0, 0, 0))
        true_probU_label = main_font.render(f"Prob U: {prob_U*0.01}", 1, (0, 0, 0))
        true_probD_label = main_font.render(f"Prob D: {prob_D*0.01}", 1, (0, 0, 0))
        #calc_val_label

        WIN.blit(true_probL_label, (10, 10))
        WIN.blit(true_probR_label, (10, true_probR_label.get_height() + 20))
        WIN.blit(true_probU_label, (10, true_probU_label.get_height() * 2 + 30))
        WIN.blit(true_probD_label, (10, true_probD_label.get_height() * 3 + 40))
        #WIN.blit(true_val_label, (WIDTH - level_label.get_widht() - 10, 10))

        L, R, U, D = calc_probab()
        print("Returned L: ", L, "R: ",R,"U: ", U, "D: ", D)
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

        pygame.display.update() #Refresh display


    while run:
        clock.tick(FPS)
        clock
        draw_window()

        #Triggering events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if (count%400 == 0):
            prob = ["L"]*prob_L + ["R"]*prob_R + ["U"]*prob_U + ["D"]*prob_D
            x = random.choice(prob)
            #print("Choice: ",x)
            car = Car(x)
            cars.append(car)
            history.append(x)

        for car in cars[:]:
            #print("Orientation: ",car.orientation)
            car.move(vel)
            count += 1

main()
