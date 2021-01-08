import pygame
from pygame.locals import *
import sys
import random
lastY = 0
gamespeed = 60
gameState = {}
class DoodleJump:
    """
    width * height = 800 * 600
    speed = [-15:15]
    agentPosX = [-60:840]
    The higher -> the (positionY) smaller
    change /* gamespeed */
    DoodleJump().run(action, posX, posY) to run
                                        action = 1 -> right
                                        action = -1 -> left
                                        action = 0 -> keep positionX
                                        posX = destinationX
                                        posY = destinationY
    dict gameState = {'agent_pos': (400, 407), 'raw_boards': [((400, 500), 0),((375, 100),1), ((87, 50), 2), ((338, 0), 3)],
                    'cameraY': 0, 'score': 0, 'agentSpeed': -14}
    raw_board: [((raw_posX, raw_posY), 0 = normal / 1 = Move_horizontal / 2 = chocolate / 3 = spring)]
    """
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont("Arial", 25)
        self.blue = pygame.image.load("assets/blue.png").convert_alpha()
        self.red = pygame.image.load("assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()
        self.direction = 0
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0

        self.clock = pygame.time.Clock()
        self.generatePlatforms()

    
    def updatePlayer(self, key):
        if not self.jump:        
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        if key == 1:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        elif key == -1:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))
    
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):
                self.jump = 50
                self.cameray -= 50

    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0,700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222,222,222), (0, x * 12), (800, x * 12))
    
    def run(self, key, posX, posY):
        self.clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.run_once(key, posX, posY)

    def run_once(self, key, posX, posY):
        """
        docstring
        """
        self.screen.fill((255,255,255))
        self.clock.tick(gamespeed)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        if self.playery - self.cameray > 700:
            self.cameray = 0
            self.score = 0
            self.springs = []
            self.platforms = [[400, 500, 0, 0]]
            self.generatePlatforms()
            self.playerx = 400
            self.playery = 400
        self.drawGrid()
        self.drawPlatforms()
        self.updatePlayer(key)
        self.updatePlatforms()
        self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
        pygame.draw.aaline(self.screen, (255, 0, 0), (self.playerx + 20, self.playery - self.cameray + 30),
                            (posX + 50, posY - self.cameray + 15), 2)
        global gameState
        gameState = {}
        global lastY
        gameState["agent_pos"] = (self.playerx, self.playery)
        gameState["raw_boards"] = []
        for board in self.platforms:
            if board[3] == 0:
                gameState["raw_boards"].append(((board[0], board[1]), board[2]))

        for spring in self.springs:
            if spring[2] == 0:
                gameState["raw_boards"].append(((board[0], board[1]), 3))

        gameState["cameraY"] = self.cameray
        gameState["score"] = self.score
        gameState["agentSpeed"] = self.playery - lastY
        lastY = self.playery

        pygame.display.flip()

if __name__ == '__main__':
    game = DoodleJump()
    game.run(1,300,0)
    game.run(-1,300,0)
    game.run(1,300,0)
    game.run(-1,300,0)

