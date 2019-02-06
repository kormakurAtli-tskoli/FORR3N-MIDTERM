# coding=utf-8
import socket
import time
from base import Base
from graphics import *

class Slave(Base):
	"""Leikmaður 2 - Slave"""

	def __init__(self, TCP_IP, TCP_PORT):
		self.matrix = [None] * 9
		self.win = self.draw()
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((TCP_IP, TCP_PORT))
			self.play()
		except Exception as e:
			print e
			self.s.close()

	def play(self):
		t = Text(Point(self.windowsize / 2, self.windowsize + 50), "")
		t.setSize(10)
		t.draw(self.win)
		while 1:
			blockid = -1
			while blockid is -1 or self.matrix[blockid] is not None:
				t.setText("Gerð þú(Smelltu til að merkja 'X'): ")
				p1mouse = self.win.getMouse()
				p1x = p1mouse.getX()
				p1y = p1mouse.getY()
				blockid = self.findblock(p1x, p1y)
			self.draw_x(blockid)
			self.matrix[int(blockid)] = "X"
			self.s.send(str(blockid))
			t.setText("Bíð eftir andstæðing...")
			data = self.s.recv(self.BUFFER_SIZE)

			if data == "WIN" or data == "DRAW":
				if data == "WIN":
					blocks = self.check("X")[0]
					p1 = self.getcenter(blocks[0])
					p2 = self.getcenter(blocks[1])
					line = Line(p1, p2)
			  		line.setFill('black')
			  		line.setWidth(5)
			  		line.draw(self.win)
					t.setText("ÞÚ VANNST")
				else:
					t.setText("JAFNTEFLI")
				t.setSize(20)
				time.sleep(3)
				self.s.close()
				break
			else:
				self.matrix[int(data)] = 'O'
				self.draw_o(self.getcenter(int(data)))
				if self.check('O')[1]:
					blocks = self.check("O")[0]
					p1 = self.getcenter(blocks[0])
					p2 = self.getcenter(blocks[1])
					line = Line(p1, p2)
			  		line.setFill('black')
			  		line.setWidth(3)
			  		line.draw(self.win)
					t.setText("ÞÚ TAPAÐIR")
					t.setSize(20)
					self.s.send("WIN")
					time.sleep(3)
					self.s.close()
					break
				if self.checkForDraw():
					t.setText("JAFNTEFLI")
					t.setSize(20)
					self.s.send("DRAW")
					time.sleep(3)
					self.s.close()
					break
