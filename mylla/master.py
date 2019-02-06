# coding=utf-8
import socket
from base import Base
from graphics import *
import time

class Master(Base):
	"""Leikmaður 1 - Master"""

	def __init__(self, TCP_IP, TCP_PORT):
		self.matrix = [None] * 9
		self.conn = None
		self.win = self.draw()
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.bind((TCP_IP, TCP_PORT))
			self.s.listen(1)
			self.play()
		except Exception as e:
			print e
			self.s.close()

	def play(self):
		try:
			t = Text(Point(self.windowsize / 2, self.windowsize + 50), "")
			t.setSize(10)
			t.draw(self.win)
			self.conn, self.addr = self.s.accept()
			print 'Tengifang:', self.addr
			while 1:
				t.setText("Bíð eftir andstæðing...")
				data = self.conn.recv(self.BUFFER_SIZE)

				if data == "WIN" or data == "DRAW":
					if data == "WIN":
						t.setText("ÞÚ VANNST")
						blocks = self.check("O")[0]
						p1 = self.getcenter(blocks[0])
						p2 = self.getcenter(blocks[1])
						line = Line(p1, p2)
				  		line.setFill('black')
				  		line.setWidth(5)
				  		line.draw(self.win)
					else:
						t.setText("JAFNTEFLI")
					t.setSize(20)
					time.sleep(3)
					self.conn.close()
					self.s.close()
					break
				else:
					self.matrix[int(data)] = 'X'
					self.draw_x(int(data))
					if self.check('X')[1]:
						t.setText("ÞÚ TAPAÐIR")
						blocks = self.check("X")[0]
						p1 = self.getcenter(blocks[0])
						p2 = self.getcenter(blocks[1])
						line = Line(p1, p2)
				  		line.setFill('black')
				  		line.setWidth(5)
				  		line.draw(self.win)
						t.setSize(20)
						self.conn.send("WIN")
						time.sleep(3)
						self.conn.close()
						self.s.close()
						break
					if self.checkForDraw():
						t.setText("JAFNTEFLI")
						t.setSize(20)
						self.conn.send("DRAW")
						time.sleep(3)
						self.conn.close()
						self.s.close()
						break
						
				blockid = -1
				while blockid is -1 or self.matrix[blockid] is not None:
					t.setText("Gerð þú(Smelltu til að merkja 'O')")
					p1mouse = self.win.getMouse()
					p1x = p1mouse.getX()
					p1y = p1mouse.getY()
					blockid = self.findblock(p1x, p1y)
				self.draw_o(self.getcenter(blockid))
				self.matrix[int(blockid)] = "O"
				self.conn.send(str(blockid))
		except Exception as e:
			print e
			self.conn.close()
			self.s.close()
