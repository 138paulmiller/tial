import sys


DEBUG = True

def error(msg):
	# print red text msg
 	sys.stderr.write('\n\033[31mPARSER ERROR: {}\033[23m'.format(str(msg)))

def debug(msg):
	if DEBUG: # print debug blue
		print '\n\033[94m{}\033[23m'.format(str(msg))


def write(msg):
	if DEBUG: # print 
		print '\033[23m{}'.format( str(msg))