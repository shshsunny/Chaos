import pygame, math

pos1 = [400, 400]
pos2 = [800, 400]
speed1 = [150, 150]
speed2 = [-300, -300]
FPS = 10
SECT = 1000 // FPS

pygame.init()

s = pygame.display.set_mode([1400, 900])
flag = True
clock = pygame.time.Clock()
while flag:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
           flag = False
    clock.tick(SECT)
    tpos1 = [math.floor(pos1[0] + 0.5),math.floor(pos1[1] + 0.5)]
    tpos2 = [math.floor(pos2[0] + 0.5),math.floor(pos2[1] + 0.5)]
    #s.fill([0, 0, 0])
    pygame.draw.circle(s, (255, 0, 0), tpos1, 20)
    pygame.draw.circle(s, (0, 0, 255), tpos2, 10)
    pygame.display.flip()


    xf = 0
    if pos2[0] < pos1[0]: xf = -1
    if pos2[0] > pos1[0]: xf = 1
    yf = 0
    if pos2[1] < pos1[1]: yf = -1
    if pos2[1] > pos1[1]: yf = 1
    try:
        speed1[0] += 1 * xf
        speed1[1] += 1 * yf
    except ZeroDivisionError:
        pass

    xf = 0
    if pos1[0] < pos2[0]: xf = -1
    if pos1[0] > pos2[0]: xf = 1
    yf = 0
    if pos1[1] < pos2[1]: yf = -1
    if pos1[1] > pos2[1]: yf = 1
    try:
        speed2[0] += 2 * xf
        speed2[1] += 2 * yf
    except ZeroDivisionError:
        pass
    
    pos1[0] += speed1[0] / SECT
    pos1[1] += speed1[1] / SECT
    pos2[0] += speed2[0] / SECT
    pos2[1] += speed2[1] / SECT
    #print("%.10f %.10f %.10f %.10f" %(ATTR[0], ATTR[1], pos[0], pos[1]))

    
pygame.quit()
