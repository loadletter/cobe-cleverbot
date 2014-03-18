#!/usr/bin/env python2
LEARN=True
ENABLEPROXY=True


if ENABLEPROXY == True:
	import socks
	import socket
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9150)
	socket.socket = socks.socksocket

import sys, time
from chatterbotapi import ChatterBotFactory, ChatterBotType
from cobe.brain import Brain


def chatbot(botname, remotebot, out=sys.stdout):
	mem = Brain(botname + ".brain")
	mem.learn("This is the only thing I know!")

	msg = "Hello!"
	out.write("BEGIN LOG: %s\n" % time.ctime())
	try:
		while True:
			out.write("Local: %s\n" % msg)
			msg = remotebot.think(msg)
			out.write("Remote: %s\n" % msg)
			if LEARN == True:
				mem.learn(msg)
			msg = mem.reply(msg)
			out.flush()

	except (KeyboardInterrupt, SystemExit, EOFError):
		print "Saving..."
		out.write("END LOG: %s\n" % time.ctime())
		out.close()

if __name__ == '__main__':
	factory = ChatterBotFactory()
	if sys.argv[1] == "clever":
		botname = "cobe_vs_clever"
		f = open(botname + ".log", "a")
		bot1 = factory.create(ChatterBotType.CLEVERBOT)
		bot1session = bot1.create_session()
		chatbot(botname, bot1session, f)
	elif sys.argv[1] == "pandora":
		botname = "cobe_vs_pandora"
		f = open(botname + ".log", "a")
		#bot1 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
		bot1 = factory.create(ChatterBotType.PANDORABOTS, '9fa364f2fe345a10') #mitsuku chatbot from mitsuku.com
		bot1session = bot1.create_session()
		bot1session.pandorabots_url = 'http://fiddle.pandorabots.com/pandora/talk-xml' #mitsuku doesn't work with the normal url
		chatbot(botname, bot1session, f)
	else:
		print "Invalid argument"
