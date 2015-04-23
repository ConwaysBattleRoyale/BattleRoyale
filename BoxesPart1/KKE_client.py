import sys, os, pygame, Image
from time import sleep
from sys import stdin, exit
from PodSixNet.Connection import connection, ConnectionListener
from thread import *
from pygame.locals import *

RED =   [(100, 0, 0),(200, 0, 0),(255, 0, 0)]
GREEN = [(0, 100, 0),(0, 200, 0),(0, 255, 0)]
BLUE =  [(0, 0, 100),(0, 0, 200),(0, 0, 255)]


class Client(ConnectionListener):
	def __init__(self, host, port):
		self.Connect((host, port))
		print "client started"
		self.move=[0,0]
		self.shooting=False
	
	def Loop(self):
		

		connection.Pump()
		self.Pump()

		for event in pygame.event.get():
			if event.type ==KEYDOWN and event.key == K_ESCAPE:
				pygame.quit()
			if event.type == KEYDOWN and event.key == K_a:
				self.move[0]-=1
			if event.type == KEYUP and event.key == K_a:
				self.move[0]+=1
			if event.type == KEYDOWN and event.key == K_d:
				self.move[0]+=1
			if event.type == KEYUP and event.key == K_d:
				self.move[0]-=1
			if event.type == KEYDOWN and event.key == K_w:
				self.move[1]-=1
			if event.type == KEYUP and event.key == K_w:
				self.move[1]+=1
			if event.type == KEYDOWN and event.key == K_s:
				self.move[1]+=1
			if event.type == KEYUP and event.key == K_s:
				self.move[1]-=1
			if event.type == MOUSEBUTTONDOWN:
				self.shooting=True
			if event.type == MOUSEBUTTONUP:
				self.shooting=False

		mousePos=pygame.mouse.get_pos()
		if self.shooting:
			shootDirection=mousePos
		else:
			shootDirection=()
		mb=25 #mouse border (ho close to edge we let mouse get)
		ss=view.size
		pygame.mouse.set_pos(self.clamp(mousePos,mb,ss[0]-mb,mb,ss[1]-mb))
		
		connection.Send({'action':'playerState','move':self.move,'shoot':shootDirection})

	def clamp(self,(x,y),xmin,xmax,ymin,ymax):
	    return [max(min(xmax, x), xmin),max(min(ymax, y), ymin)]

	def Network_setup(self,data):
		print 'setup complete!'
		view.setup(data)
		
	def Network_update(self,data):
		view.frame(data['update'])

	def Network_connected(self, data):
		print "You are now connected to the server"
	
	def Network_error(self, data):
		print 'error:', data['error'][1]
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

# Text Class Initialization
class Text():
	def __init__(self,text,color,x,y,hueVal=1):
		""" The constructor of the class """
		# Text Information
		# self.titleScreen = pygame.image.load('./KKE.png')
		self.x = x
		self.y = y
		self.text = text
		self.hueVal = hueVal
		self.clicked = False
		self.color = color
		self.font = pygame.font.SysFont('Ariel', 80, bold=True, italic=False)

	def checkX(self,mousex,area):
		if mousex >= self.x and mousex <= self.x+area[0]:
			return True

	def checkY(self,mousey,area):
		if mousey >= self.y and mousey <= self.y+area[1]:
			return True

	def checkHover(self,area):
		for event in pygame.event.get():
			pass
		mousePos = pygame.mouse.get_pos()
		mouseX = mousePos[0]
		mouseY = mousePos[1]
		boolX = self.checkX(mouseX,area)
		boolY = self.checkY(mouseY,area)
		if boolX == True and boolY == True:
			self.hueVal = 2
			return True

	def checkClicked(self,area):
		mousePos = pygame.mouse.get_pos()
		mouseX = mousePos[0]
		mouseY = mousePos[1]
		mousePress = pygame.mouse.get_pressed()
		if mousePress[0] == True:
			boolX = self.checkX(mouseX,area)
			boolY = self.checkY(mouseY,area)
			if boolX == True and boolY == True:
				self.hueVal = 0
				for event in pygame.event.get():
					if event.type == MOUSEBUTTONUP:
						self.clicked = True
				return True

	def printText(self,view):
		# print stuff
		string = str(self.text)
		area = self.font.size(string)
		# labelRect = label.get_rect()
		# labelRect.center = (self.x,self.y)

		if not self.clicked:
			if self.checkClicked(area):
				label = self.font.render(string,True,self.color[self.hueVal])
			elif self.checkHover(area):
				label = self.font.render(string,True,self.color[self.hueVal])
			else:
				self.hueVal = 1
				label = self.font.render(string,True,self.color[self.hueVal])

		view.screen.blit(label,(self.x,self.y))


class View(object):
	def __init__(self):	
		pygame.init()
		self.size=(0,0)	
		self.font = pygame.font.Font(None, 24)
		# self.titleScreen = pygame.image.load('./KKE.jpg')
		self.BLACK    = (   0,   0,   0)
		self.WHITE    = ( 255, 255, 255)
		self.GREEN    = (   25, 255,   25)
		self.RED      = ( 255,   0,   0)

	# def addTxtbtn(self,text,color,x,y):
	# 	text = Text(text,color,x,y)
	# 	return text

	def titleRunning(self):
		# self.size = data['screenSize']
		# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
		# self.screen = pygame.display.set_mode(self.size)
		self.titleBackground = pygame.image.load('./KKE.png')
		self.titleBackground = pygame.transform.scale(self.titleBackground, (self.size[0], self.size[1]))
		self.screen.blit(self.titleBackground, (0, 0))
		play = Text('Play',RED,100,500)
		while True:
			# mousePos = pygame.mouse.get_pos()
			# print mousePos[0]
			self.screen.blit(self.titleBackground, (0, 0))
			play.printText(self)
			pygame.display.flip()
			if play.clicked:
				break

	def setup(self,data):
		self.size	   = data['screenSize']
		self.playerSize= data['playerSize']
		self.zombieSize= data['zombieSize']
		self.bulletSize= data['bulletSize']
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
		self.screen   = pygame.display.set_mode(self.size)
		pygame.display.set_caption("KILL KILL Evolution")
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((250, 250, 250))
		self.screen.blit(self.background, (0, 0))
		self.titleRunning()


	def frame(self,data):
		self.screen.fill(self.WHITE)

		for player in data['players']:
			pygame.draw.rect(self.screen, self.RED,[
				player[0]-self.playerSize/2, 
				player[1]-self.playerSize/2, 
				self.playerSize,self.playerSize])
		for zombie in data['zombies']:
			pygame.draw.rect(self.screen, self.GREEN,[
				zombie[0]-self.zombieSize/2, 
				zombie[1]-self.zombieSize/2, 
				self.zombieSize,self.zombieSize])
		for bullet in data['bullets']:
			pygame.draw.rect(self.screen, self.BLACK,[
				bullet[0]-self.bulletSize/2,
				bullet[1]-self.bulletSize/2,
				self.bulletSize,self.bulletSize])
		for (i,player) in enumerate(data['players']):
			health = self.font.render(str(data['health'][i]), 1, (10, 10, 10))
			self.screen.blit(health, (player[0]-self.playerSize/4, player[1]-self.playerSize/2))
		pygame.display.flip()

if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	c = Client(host, int(port))
	view=View()
	# view.titleRunning()
	while 1:
		c.Loop()
		sleep(0.0001)