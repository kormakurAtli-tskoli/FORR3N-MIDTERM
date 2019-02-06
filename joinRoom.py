from mylla.slave import Slave
class Join(object):
	def __init__(self, master):
		self.player2 = Slave(master[0], master[1])
# Hér kæmi IP tala hjá hostinum í stað "10.220.226.61" (IP tala þeirra sem keyra hitt skjalið)
obj = Join(('10.220.226.61', 64))
