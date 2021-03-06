################################################################################################################
# Package Imports                                                                                              #
################################################################################################################
from pickle import dump,load
from pygame.locals import *
from math import *
import pygame
import random
import math
import sys
import os

################################################################################################################
# Global Variable Definitions                                                                                  #
################################################################################################################
clock = pygame.time.Clock()
pygame.font.init()
bulletList = []
# enemyList = []

# font initialization
GameOver = pygame.font.SysFont('Ariel', 140, bold=True, italic=False)
font = pygame.font.SysFont('Ariel', 80, bold=True, italic=False)

# Color Definitions
WHITE = (255, 255, 255)
GREY = (119, 136, 153)
ORANGE = (255, 102, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen Size
screenWidth = 700
screenHeight = 700
xCenter = screenWidth/2
yCenter = screenHeight/2

# Define the Screen
screen = pygame.display.set_mode((screenWidth, screenHeight))

################################################################################################################
# Class Definitions                                                                                            #
################################################################################################################

# World Class Initialization
class World():  # represents a bullet, not the game
    def __init__(self,color,x,y,width = 4,height = 4):
        """ The constructor of the class """
        self.backgrounds = []
        self.characters = []
        self.bullets = []
        self.enemys = []
        self.blocks = []
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


# Background Class Initialization
class Background():  # represents the player, not the game
    def __init__(self,color = BLACK,width = screenWidth,height = screenHeight):
        """ The constructor of the class """
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        # the background's position
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))


# Character Class Initialization
class Character():  # represents the player, not the game
    def __init__(self,color,x,y,width = 20,height = 20):
        """ The constructor of the class """
        # the character's position
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.x = x+self.width/2 + xCenter
        self.y = y+self.height/2 + yCenter
        self.xVel = 0
        self.yVel = 0
        self.xAcc = 0
        self.yAcc = 0
        self.dir = 'Up'
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        
    def getDirection(self):
        if self.xVel < 0 and self.yVel < 0:
            self.dir = 'UpLeft'
        elif self.xVel > 0 and self.yVel < 0:
            self.dir = 'UpRight'
        elif self.xVel < 0 and self.yVel > 0:
            self.dir = 'DownLeft'
        elif self.xVel > 0 and self.yVel > 0:
            self.dir = 'DownRight'
        elif self.xVel < 0:
            self.dir = 'Left'
        elif self.xVel > 0:
            self.dir = 'Right'
        elif self.yVel < 0:
            self.dir = 'Up'
        elif self.yVel > 0:
            self.dir = 'Down'


    def gameControl(self,alist):
        self.getDirection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # quit the screen
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    sys.exit() # quit the screen
                elif event.key == pygame.K_LEFT:
                    self.xVel -= 5
                elif event.key == pygame.K_RIGHT:
                    self.xVel += 5
                elif event.key == pygame.K_UP:
                    self.yVel -= 5
                elif event.key == pygame.K_DOWN:
                    self.yVel += 5
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet(GREY,0,0)
                    bullet.x = self.x+self.width/2
                    bullet.y = self.y+self.height/2

                    if self.dir == 'UpLeft':
                        bullet.xVel = -40+self.xVel
                        bullet.yVel = -40+self.yVel
                    elif self.dir == 'UpRight':
                        bullet.xVel = 40+self.xVel
                        bullet.yVel = -40+self.yVel
                    elif self.dir == 'DownLeft':
                        bullet.xVel = -40+self.xVel
                        bullet.yVel = 40+self.yVel
                    elif self.dir == 'DownRight':
                        bullet.xVel = 40+self.xVel
                        bullet.yVel = 40+self.yVel
                    elif self.dir == 'Left':
                        bullet.xVel = -40+self.xVel
                        bullet.yVel = self.yVel
                    elif self.dir == 'Right':
                        bullet.xVel = 40+self.xVel
                        bullet.yVel = self.yVel
                    elif self.dir == 'Up':
                        bullet.xVel = self.xVel
                        bullet.yVel = -40+self.yVel
                    elif self.dir == 'Down':
                        bullet.xVel = self.xVel
                        bullet.yVel = 40+self.yVel
                    alist.append(bullet)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    sys.exit() # quit the screen
                elif event.key == pygame.K_LEFT:
                    self.xVel += 5
                elif event.key == pygame.K_RIGHT:
                    self.xVel -= 5
                elif event.key == pygame.K_UP:
                    self.yVel += 5
                elif event.key == pygame.K_DOWN:
                    self.yVel -= 5

    def moveChar(self):
        self.x += self.xVel
        self.y += self.yVel
                

# Bullet Class Initialization
class Bullet():  # represents a bullet, not the game
    def __init__(self,color,x,y,width = 4,height = 4):
        """ The constructor of the class """
        # the bullet's position
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.x = x-self.width/2
        self.y = y-self.height/2
        self.xVel = 40
        self.yVel = 40
        self.bullets = {}
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        
        
# Block Class Initialization
class Block():  # represents a bullet, not the game
    def __init__(self,color,x,y,width = 4,height = 4):
        """ The constructor of the class """
        # the block's position
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.x = x-self.width/2
        self.y = y-self.height/2
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        # y = Character.self.y
        
        
# Enemy Class Initialization
class Enemy():  # represents a bullet, not the game
    def __init__(self,color,x,y,width = 4,height = 4):
        """ The constructor of the class """
        # the enemy's position
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.x = x-self.width/2
        self.y = y-self.height/2
        
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        
        
################################################################################################################
# Function Definitions                                                                                         #
################################################################################################################

def loadData():
    filename = './BattleRoyale.txt'
    data_file = open(filename,'r')
    data_list = load(data_file)
    data_file.close()
    return data_list

def saveData(alist):
    filename = './BattleRoyale.txt'
    data_file = open(filename,'w')
    dump(alist,data_file)
    data_file.close()

def drawBullets(alist):
        for bullet in alist:
            bullet.x += bullet.xVel
            bullet.y += bullet.yVel
            bullet.draw(screen)

def drawAll():
    pass

################################################################################################################
# Pre-Run Initializatio                                                                                        #
################################################################################################################
# pygame.init()
background = Background(BLACK)
character = Character(WHITE,10,10)

################################################################################################################
# Main Loop                                                                                                    #
################################################################################################################

if __name__ == "__main__": 
    while True:
        background.draw(screen)
        character.gameControl(bulletList)
        character.moveChar()
        drawBullets(bulletList)
        character.draw(screen)
        pygame.display.flip()
        clock.tick(10)
        
        
        
        
        