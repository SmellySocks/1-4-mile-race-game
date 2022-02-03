import pygame
import os

YELLOW = (255, 255, 0)
WIDTH = 720
HEIGHT = 480
METER = 16
FPS = 60


pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


clock = pygame.time.Clock()
background = pygame.image.load(os.path.join('Assets','background.png'))
vehicle = pygame.image.load(os.path.join('Assets','vehicle.png'))
bgrect = background.get_rect()
vehiclerect = vehicle.get_rect()
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("1/4 mile race")


def main():
    speed = 0
    running = True
    
    while running:
        keys = pygame.key.get_pressed()
        
        WIN.blit(background, bgrect)
        WIN.blit(background, bgrect.move(bgrect.width, 0))
        WIN.blit(vehicle,(40, HEIGHT-140))
        textsurface = myfont.render(str(round(speed*3.6)), False, (0, 0, 0))
        WIN.blit(textsurface,(0,0))
        bgrect.move_ip(METER*speed/FPS*(-1), 0)
        print (bgrect.right)
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

        print(round(speed*3.6,2))
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()

main()