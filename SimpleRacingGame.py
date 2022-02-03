import math
import pygame
import os

WIDTH = 720
HEIGHT = 480
METER = 16
FPS = 60
WHEEL_RAD = 0.32535
AERO_DRAG = 0.3
FINAL_DRIVE = 4.18
GEAR_RATIO = [0, 3.538, 1.92, 2.322, 0.975, 0.76, 0.645]
WEIGHT = 1600


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Trebuchet MS', 30)


clock = pygame.time.Clock()
background = pygame.image.load(os.path.join('Assets','background.png'))
vehicle = pygame.image.load(os.path.join('Assets','vehicle.png'))
bgrect = background.get_rect()
vehiclerect = vehicle.get_rect()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("1/4 mile race")


def main():
    speed = 0
    distance = 0
    time = 0
    qtr_mile_time = 0
    hundred_time = 0
    hundred = False
    race_finished = False
    start = False
    running = True
    block = False
    gear = 0
    torque = 100
    force = 0
    acceletarion = 0
    throttle = 0
    aero_drag = 0
    rolling_resistance = 0
    
    while running:
        keys = pygame.key.get_pressed()
        speed_surface = myfont.render(str(round(speed*3.6)) + " km/h", False, (0, 0, 0))
        dist_surface = myfont.render(str(round(distance)) + " m", False, (0, 0, 0))      #deklaracja powierzchni dystansu
        timer_surface = myfont.render(str(round(time,2)) + " s", False, (0, 0, 0))
        gear_surface = myfont.render("bieg: " + str(gear), False, (0, 0, 0))

        WIN.blit(background, bgrect)
        WIN.blit(background, bgrect.move(bgrect.width, 0))
        WIN.blit(vehicle,(40, HEIGHT-140))                  #render autka i tła
        bgrect.move_ip(METER*speed/FPS*(-1), 0)             #przesuwanie tła

        WIN.blit(speed_surface,(0,0))                       #render napisów
        WIN.blit(dist_surface,(0,30))
        WIN.blit(timer_surface,(0,60))
        WIN.blit(gear_surface,(590,0))
        
        
        
        distance = distance+speed/FPS
        if start == True:
            time = time+1/FPS

        if round(distance) == 402:
            race_finished = True
            qtr_mile_time = time
        
        if race_finished:
            print("1/4 mi: " + str(round(qtr_mile_time,2)) + " s")
            race_finished = False

        if round(speed,1) == 27.7:
            hundred = True
            hundred_time = time
        
        if hundred:
            print("0-100: " + str(round(hundred_time,2)) + " s")
            hundred = False


        if bgrect.right <= 0 and bgrect.left <= WIDTH:
            bgrect.x = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        
        if keys[pygame.K_UP]:
            start = True
            throttle=1
        else:
            throttle=0
        
        force = throttle*torque*GEAR_RATIO[gear]*FINAL_DRIVE/WHEEL_RAD
        
        rolling_resistance = WEIGHT*9.81*0.01/math.sqrt(WHEEL_RAD*WHEEL_RAD+0.01*0.01)
        aero_drag = 0.5*1.2*speed*speed*AERO_DRAG*2.61

        acceletarion = (force-rolling_resistance-aero_drag)/WEIGHT
        speed=speed+acceletarion/FPS

        if speed > 53.3:
                speed = 53.3
        if speed < 0:
                speed = 0
        
        
        if keys[pygame.K_e] and gear < len(GEAR_RATIO)-1 and block == False:
            block = True
            gear = gear+1

        if keys[pygame.K_d] and gear > 0 and block == False:
            block = True
            gear = gear-1

        if block == True and pygame.time.get_ticks()%FPS/2 == 0:
            block = False

        

        if keys[pygame.K_DOWN]:
            speed=speed-18/FPS
            if speed < 0:
                speed = 0

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()

main()