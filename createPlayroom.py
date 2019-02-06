from mylla.master import Master
class Playroom(object):
	def __init__(self, master):
		self.player1 = Master(master[0], master[1])
# Hér kæmi IP tala hjá hostinum í stað "10.220.226.61" (IP tala þeirra sem keyra þetta skjal)
obj = Playroom(('10.220.226.61', 9999))
