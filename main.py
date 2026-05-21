import pygame
import math
import random
import time

screenWidth = 700
screenHeight = 500

pygame.init()
screen = pygame.display.set_mode((screenWidth,screenHeight))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

WHITE = (255,255,255)
BLACK = (0,0,0)

class Rect:
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canColide = True
    
    def move(self, amount):
        self.y+=amount
        if self.y<0:
            self.y = 0
        if self.y+self.height>screenHeight:
            self.y = screenHeight-self.height
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def reset(self):
        self.y = screenHeight/2 - self.height/2

    def main(self):
        self.draw()

class Ball():
    def __init__(self, color, x, y, radius, speed):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.velX = 0
        self.velY = 0
        self.speed = speed
        self.setVelocity(self.speed, self.getRandomAngle())

    def getRandomAngle(self):
        return random.uniform(-math.pi/3, math.pi/3)

    def setVelocity(self, speed, angle):
        self.velX = math.cos(angle)*speed
        self.velY = math.sin(angle)*speed

    def touchingPlayerSide(self,player):
        if self.x-self.radius<= player.x+player.width and self.x+self.radius>=player.x:
            if self.y+self.radius>=player.y and self.y-self.radius<=player.y+player.height:
                return True
        return False
    
    def reset(self):
        self.x = screenWidth/2
        self.y = screenHeight/2
        for player in players:
            player.reset()
            player.draw()
        self.draw()
        pygame.display.flip()
        time.sleep(2)
        self.setVelocity(self.speed, self.getRandomAngle())

    def checkBounce(self):
        global p1Points
        global p2Points
        if self.x-self.radius<=0:
            self.velX*=-1
            p2Points+=1
            self.reset()
        if self.x+self.radius>=screenWidth:
            self.velX*=-1
            p1Points+=1
            self.reset()
        if self.y-self.radius<=0 or self.y+self.radius>=screenHeight:
            self.velY*=-1
        for player in players:
            if self.touchingPlayerSide(player):
                if player.canColide:
                    self.velX*=-1
                    player.canColide = False
            else:
                player.canColide = True
            
    def move(self):
        self.x+=self.velX
        self.y+=self.velY

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def main(self):
        self.checkBounce()
        self.move()
        self.draw()


wallDistance = 50
paddleWidth = 15
paddleHeight = 100
paddleSpeed=5

#                   X               Y             H  S
ball = Ball(WHITE, screenWidth/2, screenHeight/2, 5, 5)
p1 = Rect(WHITE, wallDistance, screenHeight/2 + paddleHeight/2, paddleWidth, paddleHeight)
p2 = Rect(WHITE, screenWidth-wallDistance-paddleWidth, screenHeight/2 + paddleHeight/2, paddleWidth, paddleHeight)
players = [p1, p2]
p1Points = 0
p2Points = 0

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BLACK)

    p1PointDisplay = font.render(str(p1Points), True, WHITE)
    p2PointDisplay = font.render(str(p2Points), True, WHITE)
    screen.blit(p1PointDisplay, (screenWidth*3/8,30))
    screen.blit(p2PointDisplay, (screenWidth*5/8,30))

    ball.main()
    for player in players:
        player.main()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p1.move(-paddleSpeed)
    if keys[pygame.K_s]:
        p1.move(paddleSpeed)
    if keys[pygame.K_UP]:
        p2.move(-paddleSpeed)
    if keys[pygame.K_DOWN]:
        p2.move(paddleSpeed)

    pygame.display.flip()
