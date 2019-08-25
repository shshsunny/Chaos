# 引入库
import pygame, math, sys, random, ctypes
pygame.init()
# 常量
try:
    GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics
    SIZE = [GetSystemMetrics(0), GetSystemMetrics(1)]
except:
    SIZE = [1366, 768]

tps = 1 # 模拟器中的时间（秒）与现实时间（秒）之比
fps = 10 # 刷新率
FILL = True
# 以下常量是游戏中的时间常量
uptime = 1000 / fps  # 游戏刷新间隔（毫秒）
def getr(m):
    return m ** 0.3 * 6#math.log(m1*80) * 5
def reset_star1():
    global m1, r1, r2, obj1, obj2, speed1
    m1 = random.randint(1, 10000)#random.randint(50, 1600)
    r1 = getr(m1)
    
    obj1 = [random.randint(0 + int(r1), SIZE[0] - int(r1)), random.randint(0+int(r1), SIZE[1]-int(r1))]
    distx = obj1[0] - obj2[0]
    disty = obj1[1] - obj2[1]
    dist = math.sqrt(distx**2+disty**2)
    if dist < (r1+r2) * 1.5: reset_star1(); return
    speed1 = [random.randint(-400, 400), random.randint(-400, 400)]
# 测试用数据


m2 = random.randint(20, 1000)
r2 = getr(m2)
obj2 = [random.randint(0 + int(r2), SIZE[0]-int(r2)), random.randint(0+int(r2), SIZE[1]-int(r2))]
speed2 = [random.randint(-400, 400), random.randint(-400, 400)]

reset_star1()
c1 = [242, 112, 34]
c2 = [154,41,133]
c3 = [125, 39, 236]
c7 = [255, 142, 255]

c4 = [18, 20, 64]
c5 = [36, 39, 128]
c6 = [151, 196, 255]

c8 = [207, 224, 234]
BACKGROUND = [6, 3, 24]
filler1 = c4[:]
filler1[0] //= 2
filler1[1] //= 2
filler1[2] //= 2
g = 20
# 函数
last = r1+r2
def fill(center, rs, re, cs, ce):  # 绘制环形渐变，rs > re
    '''默认为20层渐变'''
    pygame.draw.circle(s, cs, center, rs)
    dr = (re - rs) / 20
    dcr = (ce[0] - cs[0]) / 20
    dcg = (ce[1] - cs[1]) / 20
    dcb = (ce[2] - cs[2]) / 20
    for i in range(1, 19):
        pygame.draw.circle(s, (int(cs[0] + dcr*i), int(cs[1] + dcg*i), int(cs[2] + dcb*i)), center, int(rs + dr*i))
    pygame.draw.circle(s, ce, center, re)

    
def t(num):
    if num > 0: return 1
    if num < 0: return -1
    return 0
def set_force(): # 处理obj1受到obj2的引力
    global last, m1, m2, r1, r2, speed1, speed2
    distx = obj1[0] - obj2[0]
    disty = obj1[1] - obj2[1]
    dist = math.sqrt(distx**2+disty**2)
    if r1+r2+10 > dist: # 两星体相撞，目前默认由星体2号吸收1号
        #if dist < min(r1, r2):
        #    speed1, speed2 = [0, 0], [0, 0]  # 这里改成使用last的表达式
        s = (r1+r2 - dist) / 4# 粗略计算重合的部分线段长
        # 目标：将距离s一部分留给1号，另一部分被2号吸收，并最终使两星体相切，即r1+r2==dist
        #d1 = ((m1-m2) + math.sqrt((m1-m2)**2 + min(dist, m1))) / 2
        rawdm = 0.5*s * (r1+r2) if 0.5*s * (r1+r2) < m1 else m1 # 粗略计算被吸收的物质质量
        dm = 0
        #m2 += dm; m1 -= dm
        #newm1, newm2 = m1, m2
        while m1 >= 0  and m2 >= 0 and dm <= rawdm * 4:
            m2 += 1; m1 -= 1; dm += 1
            if not (m1 >= 0 and m2 >= 0): break
            r1 = getr(m1); r2 = getr(m2)
            if abs(dist-(r1+r2)) <= 5: break
        if m1 < 0: m1 = 0
        ns2 = []
        #ns1, ns2 = [], []
        #ns1.append((speed1[0]*m1 + speed2[0]*dm/max(m1, 1)) / (m1+dm))
        #ns1.append((speed1[1]*m1 + speed2[1]*dm/max(m1, 1)) / (m1+dm))
        ns2.append((speed2[0]*m2 + speed1[0]*dm) / (m2+dm))
        ns2.append((speed2[1]*m2 + speed1[1]*dm) / (m2+dm))
        #ns2.append((speed2[0]*m2 + speed1[0]*dm/max(m1, 1)) / (m2+dm))
        #ns2.append((speed2[1]*m2 + speed1[1]*dm/max(m1, 1)) / (m2+dm))
        speed2 = ns2
        #speed1, speed2 = ns1, ns2
        r1 = getr(m1) if m1 > 0 else 0
        r2 = getr(m2) if m2 > 0 else 0
        #print(m1, m2, m1+m2)
    #if r1 < 0: return 'quit'
    
    if r1 + r2 > 1.5*dist:
        f = int(g * m1 * m2 / last**2)
    else:
        f = int(g * m1 * m2 / max(dist, last)**2)
        last = dist
    
    if obj2[0] + r2 > SIZE[0]: speed2[0] = -abs(speed2[0]); obj2[0] = SIZE[0] - r2
    if obj2[0] - r2 < 0: speed2[0] = abs(speed2[0]); obj2[0] = r2
    if obj2[1] + r2> SIZE[1]: speed2[1] = -abs(speed2[1]); obj2[1] = SIZE[1] - r2
    if obj2[1] - r2< 0: speed2[1] = abs(speed2[1]); obj2[1] = r2
    #if dist <= r1+r2:
    #    speed2[0] += last*t(distx) / m2
    #    speed2[1] += last*t(disty) / m2
    #else:
    if m2:
        speed2[0] += f*t(distx) / m2 * tps
        speed2[1] += f*t(disty) / m2 * tps

    obj2[0] += speed2[0] / uptime * tps
    obj2[1] += speed2[1] / uptime * tps
    
    if obj1[0] + r1> SIZE[0]: speed1[0] = -abs(speed1[0]); obj1[0] = SIZE[0] - r1
    if obj1[0] - r1< 0: speed1[0] = abs(speed1[0]); obj1[0] = r1
    if obj1[1] + r1> SIZE[1]: speed1[1] = -abs(speed1[1]); obj1[1] = SIZE[1] - r1
    if obj1[1] - r1< 0: speed1[1] = abs(speed1[1]); obj1[1] = r1

    #if dist <= r1+r2:
    #    speed1[0] += -last*t(distx) / m1
    #    speed1[1] += -last*t(disty) / m1
    #else:
    if m1:
        speed1[0] += -f*t(distx) / m1 * tps
        speed1[1] += -f*t(disty) / m1 * tps
    obj1[0] += speed1[0] / uptime * tps
    obj1[1] += speed1[1] / uptime * tps
    
    #last = f
    #print(distx, disty, obj1, obj2)
# 主程序
s = pygame.display.set_mode(SIZE, pygame.RESIZABLE | pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
shotcnt = 0
while running:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
        elif i.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False
            if keys[pygame.K_LEFT]:
                m2 = m2 * 0.9
                r2 = getr(m2)
            if keys[pygame.K_RIGHT]:
                m2 = m2 * 1.1
                r2 = getr(m2)
            if keys[pygame.K_a]:
                m1 = m1 * 0.9
                r1 = getr(m1)
            if keys[pygame.K_d]:
                m1 = m1 * 1.1
                r1 = getr(m1)
            if keys[pygame.K_s]:
                m2 = m1
                r2 = getr(m2)
    clock.tick(uptime)
    if FILL: s.fill(BACKGROUND)
    #if r1 < 0: break
    #pygame.draw.rect(s, (0, 0, 0), [0, 0, SIZE[0], SIZE[1]])
    pos1 = [int(obj1[0] + 0.5), int (obj1[1] + 0.5)]
    pos2 = [int(obj2[0] + 0.5), int (obj2[1] + 0.5)]
    if m1:
        fill(pos1, abs(int(r1)), abs(int(r1 / 1.1)), c4, c5)
        fill(pos1, abs(int(r1 / 1.1)), abs(int(r1 / 2)), c5, c6)
       #pygame.draw.circle(s, c4, pos1, abs(int(r1)))
        #pygame.draw.circle(s, c5, pos1, abs(int(r1 / 1.1)))
        #pygame.draw.circle(s, c6, pos1, abs(int(r1 / 1.5)))
    fill(pos2, int(r2), int(r2 * 0.75), filler1, c1)
   # fill(pos2, int(r2), int(r2 * 3 / 4), c1, c2)
    fill(pos2, int(r2 * 0.75), int(r2 / 2.5), c2, c3)
    #fill(pos2, int(r2 / 2.5), int(r2 / 16), c3, c7)
    #pygame.draw.circle(s, c1, pos2, int(r2))
    #pygame.draw.circle(s, c2, pos2, int(r2 * 3 / 4))
    pygame.draw.circle(s, c3, pos2, int(r2 / 2.5))
    pygame.draw.circle(s, c7, pos2, int(r2 / 16))
    pygame.display.flip()
    if set_force() == 'quit':
        running = False
    if m1 == 0:  # 重设一次
        reset_star1()

    #if m2 <= 1:
    #    print("Sun shrinked out!")
    #    break
    #m2 *= 0.995
    #m1 *= 1.005
    #r1 = getr(m1)
    #r2 = getr(m2)
    
pygame.quit()
