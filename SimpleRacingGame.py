import pygame
import os

YELLOW = (255, 255, 0)
WIDTH = 720
HEIGHT = 480
METER = 16
FPS = 60


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
    running = True
    
    while running:
        keys = pygame.key.get_pressed()
        speed_surface = myfont.render(str(round(speed*3.6)) + " km/h", False, (0, 0, 0))
        dist_surface = myfont.render(str(round(distance)) + " m", False, (0, 0, 0))      #deklaracja powierzchni dystansu
        timer_surface = myfont.render(str(round(time,2)) + " s", False, (0, 0, 0))

        WIN.blit(background, bgrect)
        WIN.blit(background, bgrect.move(bgrect.width, 0))
        WIN.blit(vehicle,(40, HEIGHT-140))                  #render autka i tła
        bgrect.move_ip(METER*speed/FPS*(-1), 0)             #przesuwanie tła

        WIN.blit(speed_surface,(0,0))                       #render napisów
        WIN.blit(dist_surface,(0,30))
        WIN.blit(timer_surface,(0,60))
        
        distance = distance+speed/FPS
        time = time+1/FPS

        if bgrect.right <= 0 and bgrect.left <= WIDTH:
            bgrect.x = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        if keys[pygame.K_UP]:
            speed=speed+2.24/FPS
            if speed > 53.3:
                speed=53.3

        else:
            speed=speed-2.24/FPS
            if speed < 0:
                speed = 0

        if keys[pygame.K_DOWN]:
            speed=speed-18/FPS
            if speed < 0:
                speed = 0
                
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()

main()