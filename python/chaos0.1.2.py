import pygame, math

# constants
pos1 = [400, 400]
pos2 = [400, 200]
speed1 = [-150, 0]
speed2 = [300, 0]
r1 = 50
r2 = 25
FPS = 25
SECT = 1000 // FPS
g =80
# functions
def calc(x1, x2, y1, y2, r1, r2):
    dist = ((x1-x2)**2+(y1-y2)**2)
    
    res = g ** 2 * r1 * r2 / dist
    if dist < r1 + r2:
        res /= dist * g
    if dist < 1:
        res = 0
    return res
# program running

pygame.init()

s = pygame.display.set_mode([1400, 1000], pygame.RESIZABLE)
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
    pygame.draw.circle(s, (255, 0, 0), tpos1, int(math.sqrt(r1 / math.pi) * 5))
    pygame.draw.circle(s, (0, 0, 255), tpos2, int(math.sqrt(r2 / math.pi) * 5))
    pygame.display.flip()


    pos2[0] += speed2[0] / SECT
    pos2[1] += speed2[1] / SECT
    pos1[0] += speed1[0] / SECT
    pos1[1] += speed1[1] / SECT
    
    force = calc(pos1[0], pos2[0], pos1[1], pos2[1], r1, r2)

    xf = 0
    if pos2[0] < pos1[0]: xf = -1
    if pos2[0] > pos1[0]: xf = 1
    yf = 0
    if pos2[1] < pos1[1]: yf = -1
    if pos2[1] > pos1[1]: yf = 1
    
    speed1[0] += force * xf / r1
    speed1[1] += force * yf / r1

    xf = 0
    if pos1[0] < pos2[0]: xf = -1
    if pos1[0] > pos2[0]: xf = 1
    yf = 0
    if pos1[1] < pos2[1]: yf = -1
    if pos1[1] > pos2[1]: yf = 1
    
    speed2[0] += force * xf / r2
    speed2[1] += force * yf / r2

    #print("%.10f %.10f %.10f %.10f" %(ATTR[0], ATTR[1], pos[0], pos[1]))

    
pygame.quit()
