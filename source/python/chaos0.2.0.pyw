# 引入库
import pygame, math, sys, random
pygame.init()

# 常量
SIZE = [1366, 768]
tps = 1 # 模拟器中的时间（秒）与现实时间（秒）之比
fps = 15 # 刷新率
# 以下常量是游戏中的时间常量
uptime = 1000 / fps / tps  # 游戏刷新间隔（毫秒）

# 测试用数据

m1 = random.randint(50, 1600)
m2 = random.randint(50, 1600)
r1 = math.sqrt(m1) * 2
r2 = math.sqrt(m2) * 2
obj1 = [random.uniform(0 + r1, SIZE[0] - r1), random.uniform(0+r1, SIZE[1]-r1)]
obj2 = [random.uniform(0 + r2, SIZE[0]-r2), random.uniform(0+r2, SIZE[1]-r2)]
speed1 = [random.randint(-200, 200), random.randint(-200, 200)]
speed2 = [random.randint(-200, 200), random.randint(-200, 200)]
c1 = [239,106,5]
c2 = [128,40,179]
c3 = [249,160,76]
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
    if dist <= r1+r2:
        f = g * m1 * m2 / (r1+r2)**2
        #f = last
    else: 
        f = g * m1 * m2 / dist**2
    
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

    obj2[0] += speed2[0] / uptime
    obj2[1] += speed2[1] / uptime
    
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
    obj1[0] += speed1[0] / uptime
    obj1[1] += speed1[1] / uptime
    #last = f
    #print(distx, disty, obj1, obj2)

# 主程序
s = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        if i.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
    clock.tick(uptime)
    s.fill([0, 0, 0])
    pos1 = [int(obj1[0] + 0.5), int (obj1[1] + 0.5)]
    pos2 = [int(obj2[0] + 0.5), int (obj2[1] + 0.5)]
    pygame.draw.circle(s, c1, pos1, int(r1))
    pygame.draw.circle(s, c2, pos1, int(r1 / 1.4))
    pygame.draw.circle(s, c3, pos1, int(r1 / 10))
    pygame.draw.circle(s, c1, pos2, int(r2))
    pygame.draw.circle(s, c2, pos2, int(r2 / 1.4))
    pygame.draw.circle(s, c3, pos2, int(r2 / 10))
    pygame.display.flip()
    set_force()
pygame.quit()
