import pygame, math

ATTR = [600, 400]
pos = [300, 300]
speed = [0, 200]
FPS = 25
SECT = 1000 // FPS

pygame.init()

s = pygame.display.set_mode([1300, 800], pygame.RESIZABLE)
flag = True
clock = pygame.time.Clock()
while flag:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
           flag = False
    clock.tick(SECT)
    tpos = [math.floor(pos[0] + 0.5),math.floor(pos[1] + 0.5)]
    s.fill([0, 0, 0])
    pygame.draw.circle(s, (255, 255, 255), tpos, 10)
    pygame.draw.circle(s, (255, 0, 0), ATTR, 10)
    pygame.display.flip()


    xf = 1
    if ATTR[0] < pos[0]: xf = -1
    yf = 1
    if ATTR[1] < pos[1]: yf = -1
    try:
        speed[0] += 3 * xf
        speed[1] += 3 * yf
    except ZeroDivisionError:
        pass
    
    pos[0] += speed[0] / SECT
    pos[1] += speed[1] / SECT
    #print("%.10f %.10f %.10f %.10f" %(ATTR[0], ATTR[1], pos[0], pos[1]))

    
pygame.quit()
