import sys
from time import sleep
from sys import stdin, exit
from PodSixNet.Connection import connection, ConnectionListener
from thread import *
import pygame
from pygame.locals import *

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
			if event.type == KEYDOWN and event.key == K_LEFT:
				self.move[0]-=1
			if event.type == KEYUP and event.key == K_LEFT:
				self.move[0]+=1
			if event.type == KEYDOWN and event.key == K_RIGHT:
				self.move[0]+=1
			if event.type == KEYUP and event.key == K_RIGHT:
				self.move[0]-=1
			if event.type == KEYDOWN and event.key == K_UP:
				self.move[1]-=1
			if event.type == KEYUP and event.key == K_UP:
				self.move[1]+=1
			if event.type == KEYDOWN and event.key == K_DOWN:
				self.move[1]+=1
			if event.type == KEYUP and event.key == K_DOWN:
				self.move[1]-=1
			if event.type == MOUSEBUTTONDOWN:
				self.shooting=True
			if event.type == MOUSEBUTTONUP:
				self.shooting=False
		if self.shooting:
			shootDirection=pygame.mouse.get_pos()
		else:
			shootDirection=()
		connection.Send({'action':'playerState','move':self.move,'shoot':shootDirection})

	def Network_setup(self,data):
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

class View(object):
	def __init__(self):	
		pygame.init()	
		self.BLACK    = (   0,   0,   0)
		self.WHITE    = ( 255, 255, 255)
		self.GREEN    = (   0, 255,   0)
		self.RED      = ( 255,   0,   0)

 	def setup(self,data):
 		self.size	   = data['screenSize']
 		self.playerSize= data['playerSize']
 		self.zombieSize= data['zombieSize']
 		self.bulletSize= data['bulletSize']
		self.screen   = pygame.display.set_mode(self.size)
		pygame.display.set_caption("KILL KILL Evolution")

	def frame(self,data):
		self.screen.fill(self.WHITE)

		for player in data['players']:
			pygame.draw.rect(self.screen, self.RED,[
				player[0]-self.playerSize/2, 
				player[1]-self.playerSize/2, 
				self.playerSize,self.playerSize])
		for zombie in data['zombies']:
			pygame.draw.rect(self.screen, self.BLACK,[
				zombie[0]-self.zombieSize/2, 
				zombie[1]-self.zombieSize/2, 
				self.zombieSize,self.zombieSize])
		for bullet in data['bullets']:
			pygame.draw.rect(self.screen, self.GREEN,[
				bullet[0]-self.bulletSize/2,
				bullet[1]-self.bulletSize/2,
				self.bulletSize,self.bulletSize])
		pygame.display.flip()

if len(sys.argv) != 2:
	print "Usage:", sys.argv[0], "host:port"
	print "e.g.", sys.argv[0], "localhost:31425"
else:
	host, port = sys.argv[1].split(":")
	c = Client(host, int(port))
	view=View()
	while 1:
		c.Loop()
		sleep(0.0001)