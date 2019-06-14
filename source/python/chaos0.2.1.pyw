# 引入库
import pygame, math, sys, random
pygame.init()

# 常量
SIZE = [1366, 768]
tps = 1 # 模拟器中的时间（秒）与现实时间（秒）之比
fps = 15 # 刷新率
# 以下常量是游戏中的时间常量
uptime = 1000 / fps  # 游戏刷新间隔（毫秒）

# 测试用数据

m1 = random.randint(50, 200)#random.randint(50, 1600)
m2 = random.randint(1000, 2000)
r1 = math.log(m1*20) * 5
r2 = math.log(m2*20) * 5
obj1 = [random.randint(0 + int(r1), SIZE[0] - int(r1)), random.randint(0+int(r1), SIZE[1]-int(r1))]
obj2 = [random.randint(0 + int(r2), SIZE[0]-int(r2)), random.randint(0+int(r2), SIZE[1]-int(r2))]
speed1 = [random.randint(-300, 300), random.randint(-300, 300)]
speed2 = [random.randint(-300, 300), random.randint(-300, 300)]
c1 = [239,106,5]
c2 = [128,40,179]
c3 = [249,160,76]
c4 = [35, 111, 231]
c5 = [193, 44, 146]
c6 = [255, 64, 174]
g = 50
# 函数
#last = 0
def t(num):
    if num > 0: return 1
    if num < 0: return -1
    return 0
def set_force(): # 处理obj1受到obj2的引力
    global last
    distx = obj1[0] - obj2[0]
    disty = obj1[1] - obj2[1]
    dist = math.sqrt(distx**2+disty**2)
    f = int(g * m1 * m2 / max(dist, r1+r2)**2 * tps)
    
    if obj2[0] + r2 > SIZE[0]: speed2[0] = -abs(speed2[0])
    elif obj2[0] - r2 < 0: speed2[0] = abs(speed2[0])
    if obj2[1] + r2> SIZE[1]: speed2[1] = -abs(speed2[1])
    elif obj2[1] - r2< 0: speed2[1] = abs(speed2[1])    
    #if dist <= r1+r2:
    #    speed2[0] += last*t(distx) / m2
    #    speed2[1] += last*t(disty) / m2
    #else:
    speed2[0] += f*t(distx) / m2
    speed2[1] += f*t(disty) / m2

    obj2[0] += speed2[0] / uptime * tps
    obj2[1] += speed2[1] / uptime * tps
    
    if obj1[0] + r1> SIZE[0]: speed1[0] = -abs(speed1[0])
    elif obj1[0] - r1< 0: speed1[0] = abs(speed1[0])
    if obj1[1] + r1> SIZE[1]: speed1[1] = -abs(speed1[1])
    elif obj1[1] - r1< 0: speed1[1] = abs(speed1[1])

    #if dist <= r1+r2:
    #    speed1[0] += -last*t(distx) / m1
    #    speed1[1] += -last*t(disty) / m1
    #else:
    
    speed1[0] += -f*t(distx) / m1
    speed1[1] += -f*t(disty) / m1
    obj1[0] += speed1[0] / uptime * tps
    obj1[1] += speed1[1] / uptime * tps
    
    #last = f
    #print(distx, disty, obj1, obj2)

# 主程序
s = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
upt = 0
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
    clock.tick(uptime)
    #s.fill([0, 0, 0])
    #upt += uptime
    #if upt >= 50000:
    #    s.fill([0, 0, 0])
    #    upt = 0
    #pygame.draw.rect(s, (0, 0, 0), [0, 0, SIZE[0], SIZE[1]])
    pos1 = [int(obj1[0] + 0.5), int (obj1[1] + 0.5)]
    pos2 = [int(obj2[0] + 0.5), int (obj2[1] + 0.5)]
    pygame.draw.circle(s, c1, pos1, int(r1))
    pygame.draw.circle(s, c2, pos1, int(r1 / 1.4))
    pygame.draw.circle(s, c3, pos1, int(r1 / 10))
    pygame.draw.circle(s, c4, pos2, int(r2))
    pygame.draw.circle(s, c5, pos2, int(r2 / 1.4))
    pygame.draw.circle(s, c6, pos2, int(r2 / 10))
    pygame.display.flip()
    set_force()
pygame.quit()
