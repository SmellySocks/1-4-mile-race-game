import math
from operator import ge
import pygame
import os

WIDTH = 720
HEIGHT = 480
METER = 16
FPS = 60
WHEEL_RAD = 0.32535
AERO_DRAG = 0.3
FINAL_DRIVE = 4.47
GEAR_RATIO = [0, 3.417, 1.783, 1.121, 0.795, 0.647, 0.534]
TORQUE = [150, 160, 185, 260, 330, 370, 360, 355, 350, 340, 325, 300, 275, 260, 255, 0]
WEIGHT = 1600


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Lucida Console', 30)


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
    torque = 0
    force = 0
    acceletarion = 0
    throttle = 0
    aero_drag = 0
    rolling_resistance = 0
    eng_RPM = 750
    wheel_RPM = 0

    
    while running:
        keys = pygame.key.get_pressed()
        speed_surface = myfont.render(str(round(speed*3.6)) + " km/h", True, (0, 0, 0))
        dist_surface = myfont.render(str(round(distance)) + " m", True, (0, 0, 0))      #deklaracja powierzchni dystansu
        timer_surface = myfont.render(str(round(time,2)) + " s", True, (0, 0, 0))
        gear_surface = myfont.render("bieg: " + str(gear), True, (0, 0, 0))
        RPM_surface = myfont.render("RPM: " + str(round(eng_RPM)), True, (0, 0, 0))

        WIN.blit(background, bgrect)
        WIN.blit(background, bgrect.move(bgrect.width, 0))
        WIN.blit(vehicle,(40, HEIGHT-140))                  #render autka i tła
        bgrect.move_ip(METER*speed/FPS*(-1), 0)             #przesuwanie tła

        WIN.blit(speed_surface,(0,0))                       #render napisów
        WIN.blit(dist_surface,(0,30))
        WIN.blit(timer_surface,(0,60))
        WIN.blit(gear_surface,(590,0))
        WIN.blit(RPM_surface,(560,30))
        
        
        
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
            hundred_time = time
            print("0-100: " + str(round(hundred_time,2)) + " s")


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
        
        torque = TORQUE[round(eng_RPM/250)-2]

        force = throttle*torque*GEAR_RATIO[gear]*FINAL_DRIVE/WHEEL_RAD

        rolling_resistance = WEIGHT*9.81*0.01/math.sqrt(WHEEL_RAD*WHEEL_RAD+0.01*0.01)
        aero_drag = 0.5*1.2*speed*speed*AERO_DRAG*2.61

        acceletarion = (force-rolling_resistance-aero_drag)/WEIGHT
        speed=speed+acceletarion/FPS

        wheel_RPM = speed/((WHEEL_RAD*2*math.pi)/60)
        eng_RPM = wheel_RPM*GEAR_RATIO[gear]*FINAL_DRIVE

        if speed > 53.3:
                speed = 53.3
        if speed < 0:
                speed = 0
        if eng_RPM < 750:
            print("Silnik gaśnie")
            eng_RPM = 750
        if eng_RPM > 4250:
            print("Odcina!")
            eng_RPM = 4250
        
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