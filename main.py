import math, random, copy, pygame, sys, sympy

WHITE   =  (255, 255, 255)
ORANGE  =  (255, 127, 0  )
YELLOW  =  (255, 255, 0  )
BLACK   =  (0,   0,   0  )
BLUE    =  (0,   0,   255)
RED     =  (255, 0,   0  )
SKYBLUE =  (135, 206, 235)
SLIVER  =  (192, 192, 192)
BROWN   =  (206, 139, 84 )

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

SPEED = 5

pygame.init()
pygame.display.set_caption("미적분")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def getDistance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

class RoundSquare:
    def __init__(self,x,y,size) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.skin = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        pygame.draw.rect(self.skin, ORANGE, pygame.Rect(self.size*1/4, self.size*1/4, self.size*2/4, self.size*2/4))
        pygame.draw.rect(self.skin, ORANGE, pygame.Rect(self.size*1/4,             0, self.size*2/4, self.size*1/4))
        pygame.draw.rect(self.skin, ORANGE, pygame.Rect(self.size*1/4, self.size*3/4, self.size*2/4, self.size*1/4))
        pygame.draw.rect(self.skin, ORANGE, pygame.Rect(            0, self.size*1/4, self.size*1/4, self.size*2/4))
        pygame.draw.rect(self.skin, ORANGE, pygame.Rect(self.size*3/4, self.size*1/4, self.size*1/4, self.size*2/4))
        pygame.draw.circle(self.skin, ORANGE, (self.size*1/4, self.size*1/4), self.size/4, 0)
        pygame.draw.circle(self.skin, ORANGE, (self.size*3/4, self.size*1/4), self.size/4, 0)
        pygame.draw.circle(self.skin, ORANGE, (self.size*1/4, self.size*3/4), self.size/4, 0)
        pygame.draw.circle(self.skin, ORANGE, (self.size*3/4, self.size*3/4), self.size/4, 0)

    def draw(self,screen):
        screen.blit(self.skin,(self.x-self.size/2,self.y-self.size/2))

class Player:
    def __init__(self,x,y,size) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.skin = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        pygame.draw.circle(self.skin, RED, (self.size*2/4, self.size*2/4), self.size/4, 0)

    def draw(self,screen):
        screen.blit(self.skin,(self.x-self.size/2,self.y-self.size/2))

class Line:
    def __init__(self, incline, x,y) -> None:
        self.incline = incline
        self.x = x
        self.y = y
    
    def getY(self, x):
        return self.incline * (x - self.x) + self.y

    def getX(self, y):
        return (y - self.y + self.incline * self.x)/(self.incline + 2e-16)

    def getPoint(self, line):
        m1 = self.incline
        m2 = line.incline
        t1 = self.x
        t2 = line.x
        p1 = self.y
        p2 = line.y
        x = (t1*m1 - t2*m2 + p2 - p1)/(m1-m2)
        return (x, self.getY(x))
    
    def getDistance(self,x, y):
        return abs(self.incline * x - y - self.incline * self.x + self.y)/math.sqrt(self.incline ** 2 + 1)
    
    def draw(self,screen):
        pygame.draw.line(screen, RED, (self.x, self.y), (self.x + 1000, self.y + 1000*self.incline), 1)
        pygame.draw.line(screen, RED, (self.x, self.y), (self.x - 1000, self.y - 1000*self.incline), 1)

def getIndexPosition(square,index):
    x = square.x - square.size/4 + 2 * index[0] * square.size/4
    y = square.y - square.size/4 + 2 * index[1] * square.size/4
    return x,y

def getIncline(square, player, index):
    x = square.x - square.size/4 + 2 * index[0] * square.size/4
    y = square.y - square.size/4 + 2 * index[1] * square.size/4
    l = getDistance((x, y), (player.x, player.y))
    r = square.size/4
    tanTheta = r/math.sqrt(l**2 - r**2)
    tanP = (y - player.y)/(x - player.x + 2e-16)
    incline1 = (tanP - tanTheta) / (1 + tanTheta * tanP + 2e-16)
    incline2 = (tanP + tanTheta) / (1 - tanTheta * tanP + 2e-16)
    return incline1, incline2

def getDegree(square, player, index):
    x = square.x - square.size/4 + 2 * index[0] * square.size/4
    y = square.y - square.size/4 + 2 * index[1] * square.size/4
    l = getDistance((x, y), (player.x, player.y))
    r = square.size/4
    theta = math.atan(r/math.sqrt(l**2 - r**2))
    p = math.atan((y - player.y)/(x - player.x))
    return theta - p, theta + p

def checker(incline, player, square):
    line = Line(incline, player.x, player.y)
    maxDistance = -math.inf
    secDistance = -math.inf
    distanceSave = [(0,0),(0,0)]
    for i in range(2):
        for j in range(2):
            distance = line.getDistance(square.x, square.y)
            circle = (square.x - square.size/4 + 2 * i * square.size/4, square.y - square.size/4 + 2 * j * square.size/4)
            degree = math.atan(-1/incline)
            radius = square.size/4
            pos = (circle[0] + radius * math.cos(degree) , circle[1] + radius * math.sin(degree))
            if maxDistance < distance:
                maxDistance = distance
                distanceSave[0] = pos
            elif secDistance < distance:
                secDistance = distance
                distanceSave[1] = pos
    return tuple(distanceSave)

def getRipeIncline(square, player):
    result = []
    print("=========")
    for i in range(2):
        for j in range(2):
            incline = getIncline(square, player, (i, j))
            result.append(incline[0])
            result.append(incline[1])

    return result

def getEveryIncline(square, player, Ishash = False):
    if not Ishash:
        result = [[],[]]
        for i in range(2):
            for j in range(2):
                result[i].append(getIncline(square, player, (i,j)))
        return result
    else:
        result = [0,0]
        maxDistance = -math.inf
        secDistance = -math.inf
        distanceSave = [(0,0),(0,0)]
        print("=========")
        for i in range(2):
            print(f"({i})=========")
            for j in range(2):
                print(f"({j})=========")
                for incline in getIncline(square, player, (i, j)):
                    line = Line(incline, player.x, player.y)
                    distance = line.getDistance(square.x, square.y)
                    print(distance)
                    circle = (square.x - square.size/4 + 2 * i * square.size/4, square.y - square.size/4 + 2 * j * square.size/4)
                    degree = math.atan(-1/(incline+2e-16))
                    radius = square.size/4
                    pos = (circle[0] + radius * math.cos(degree) * (-1)**(square.x < player.x) , circle[1] + radius * math.sin(degree) * (-1)**(square.y > player.y) )
                    if maxDistance < distance:
                        maxDistance = distance
                        result[0] = incline
                        distanceSave[0] = (circle[0] - radius * math.cos(degree) , circle[1] - radius * math.sin(degree))
                    elif secDistance < distance:
                        secDistance = distance
                        result[1] = incline
                        distanceSave[1] = (circle[0] - radius * math.cos(degree) , circle[1] - radius * math.sin(degree))

        return result, distanceSave

def getRealIncline(square, player):
    radius = square.size/4
    print(player.x, player.y)
    if player.x < square.x - square.size/2 or player.x > square.x + square.size/2 :
        pos = [(0,0), (0,0)]
        inclineList = getRipeIncline(square, player)
        maxIncline = inclineList.index(max(inclineList))
        minIncline = inclineList.index(min(inclineList))
        maxIndex = (maxIncline//2, maxIncline%2)
        minIndex = (minIncline//2, minIncline%2)
        temp = getIndexPosition(square, maxIndex)
        pos[0] = Line(max(inclineList), player.x, player.y).getPoint(Line(-1/(max(inclineList)+2e-16), temp[0], temp[1]))
        temp = getIndexPosition(square, minIndex)
        pos[1] = Line(min(inclineList), player.x, player.y).getPoint(Line(-1/(min(inclineList)+2e-16), temp[0], temp[1]))
        print("case1")
        return [max(inclineList), min(inclineList)], pos
    elif square.x - square.size/2 <= player.x <= square.x + square.size/2 and square.y + square.size/2 <= player.y:
        print("case2-1")
        result = [0,0]
        pos = [(0,0), (0,0)]
        maxDistance = -math.inf
        for incline in getIncline(square, player, (0, 1)):
            line = Line(incline, player.x, player.y)
            distance = line.getDistance(square.x, square.y)
            if maxDistance < distance:
                maxDistance = distance
                result[0] = incline
                temp = getIndexPosition(square, (0,1))
                pos[0] = line.getPoint(Line(-1/(incline+2e-16), temp[0], temp[1]))
        maxDistance = -math.inf
        for incline in getIncline(square, player, (1, 1)):
            line = Line(incline, player.x, player.y)
            distance = line.getDistance(square.x, square.y)
            if maxDistance < distance:
                maxDistance = distance
                result[1] = incline
                temp = getIndexPosition(square, (1,1))
                pos[1] = line.getPoint(Line(-1/(incline+2e-16), temp[0], temp[1]))

        return result, pos
    
    elif square.x - square.size/2 <= player.x <= square.x + square.size/2 and square.y - square.size/2 >= player.y:
        print("case2-2")
        result = [0,0]
        pos = [(0,0), (0,0)]
        maxDistance = -math.inf
        for incline in getIncline(square, player, (0, 0)):
            line = Line(incline, player.x, player.y)
            distance = line.getDistance(square.x, square.y)
            if maxDistance < distance:
                maxDistance = distance
                result[0] = incline
                temp = getIndexPosition(square, (0,0))
                pos[0] = line.getPoint(Line(-1/(incline+2e-16), temp[0], temp[1]))

        maxDistance = -math.inf
        for incline in getIncline(square, player, (1, 0)):
            line = Line(incline, player.x, player.y)
            distance = line.getDistance(square.x, square.y)
            if maxDistance < distance:
                maxDistance = distance
                result[1] = incline
                temp = getIndexPosition(square, (1,0))
                pos[1] = line.getPoint(Line(-1/(incline+2e-16), temp[0], temp[1]))

        return result, pos

    elif square.x - square.size/2 <= player.x <= square.x - square.size/2 + radius and square.y - square.size/2 <= player.y <= square.y - square.size/2 + radius:
        print("case3-1")
        pos = [(0,0),(0,0)]
        inclines = getIncline(square, player, (0, 0))
        temp = getIndexPosition(square, (0, 0))
        pos[0] = Line(inclines[0], player.x, player.y).getPoint(Line(-1/(inclines[0]+2e-16), temp[0], temp[1]))
        pos[1] = Line(inclines[1], player.x, player.y).getPoint(Line(-1/(inclines[0]+2e-16), temp[0], temp[1]))
        return inclines, pos
    elif square.x - square.size/2 <= player.x <= square.x - square.size/2 + radius and square.y + square.size/2 - radius <= player.y <= square.y + square.size/2:
        print("case3-2")
        pos = [(0,0),(0,0)]
        inclines = getIncline(square, player, (0, 1))
        temp = getIndexPosition(square, (0, 1))
        pos[0] = Line(inclines[0], player.x, player.y).getPoint(Line(-1/(inclines[0]+2e-16), temp[0], temp[1]))
        pos[1] = Line(inclines[1], player.x, player.y).getPoint(Line(-1/(inclines[0]+2e-16), temp[0], temp[1]))
        return inclines, pos
    elif square.x + square.size/2 - radius <= player.x <= square.x + square.size/2 and square.y - square.size/2 <= player.y <= square.y - square.size/2 + radius:
        print("case3-3")
        pos = [(0,0),(0,0)]
        inclines = getIncline(square, player, (1, 0))
        temp = getIndexPosition(square, (1, 1))
        pos[0] = Line(inclines[0], player.x, player.y).getPoint(Line(-1/(inclines[0]+2e-16), temp[0], temp[1]))
        pos[1] = Line(inclines[1], player.x, player.y).getPoint(Line(-1/(inclines[0]+2e-16), temp[0], temp[1]))
        return inclines, pos
    elif square.x + square.size/2 - radius <= player.x <= square.x + square.size/2 and square.y + square.size/2 - radius <= player.y <= square.y + square.size/2:
        print("case3-4")
        pos = [(0,0),(0,0)]
        inclines = getIncline(square, player, (1, 1))
        temp = getIndexPosition(square, (1, 1))
        pos[0] = Line(inclines[0], player.x, player.y).getPoint(Line(-1/(inclines[0]+2e-16), temp[0], temp[1]))
        pos[1] = Line(inclines[1], player.x, player.y).getPoint(Line(-1/(inclines[0]+2e-16), temp[0], temp[1]))
        return inclines, pos
    else:
        print("case4")
        inclineList = getRipeIncline(square, player)
        return max(inclineList), min(inclineList)

def getEveryLine(square, player):
    result = [[],[]]
    for i in range(2):
        for j in range(2):
            one, two = getIncline(square, player, (i,j))
            result[i].append([Line(one, player.x, player.y), Line(two, player.x, player.y)])
    return result

square = RoundSquare(500, 250, 300)
player = Player(0, 0, 20)

while True:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        player.y -= SPEED
    if pressed[pygame.K_DOWN]:
        player.y += SPEED
    if pressed[pygame.K_RIGHT]:
        player.x += SPEED
    if pressed[pygame.K_LEFT]:
        player.x -= SPEED
    screen.fill(WHITE)
    temp = getRealIncline(square, player)
    inclineList = temp[0]
    posList = temp[1]
    DISTANCE = 1000
    a = Line(inclineList[0],player.x,player.y).getY(SCREEN_WIDTH)
    b = Line(inclineList[1],player.x,player.y).getY(SCREEN_WIDTH)
    point1 = None
    if a > b:
        point1 = (SCREEN_WIDTH,a)
    else:
        point1 = (SCREEN_WIDTH,b)
    a = Line(inclineList[0],player.x,player.y).getX(SCREEN_HEIGHT)
    b = Line(inclineList[1],player.x,player.y).getX(SCREEN_HEIGHT)
    point2 = None
    if a > b:
        point2 = (b,SCREEN_HEIGHT)
    else:
        point2 = (a,SCREEN_HEIGHT)

    #pygame.draw.polygon(screen,BLACK,[posList[0], posList[1], point1, point2],0)
    #pygame.draw.polygon(screen,BLACK,[posList[1],posList[0],(player.x + DISTANCE, player.y + DISTANCE * inclineList[0]), (player.x + DISTANCE, player.y + DISTANCE * inclineList[1])],0)
    square.draw(screen)
    #pygame.draw.polygon(screen,BLACK,[posList[0],posList[1],(player.x + 1000, player.y + 1000 * max(inclineList)), (player.x + 1000, player.y + 1000 * min(inclineList))],0)
    for i in inclineList: Line(i,player.x,player.y).draw(screen)
    #Line(max(inclineList),player.x,player.y).draw(screen)
    #Line(min(inclineList),player.x,player.y).draw(screen)
    player.draw(screen)

    pygame.display.update()