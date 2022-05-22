"""
For the moment, just a read-parse-print loop.

"""
import os
from bedspread import __version__, syntax, front_end

def promptedInput():
	# Prompt for some input:
	return input("Ready >> ")

def display(aTree):
	# Eventually walk an AST and pretty-print the result.
	print(aTree)

def usage():
	print("Bed Spread (version %s), interactive REPL"% __version__)
	print("    Documentation is at http://bedspread.readthedocs.io")
	print("    Follow progress at https://github.com/kjosib/bedspread")
	print("    This is pre-alpha code. Current goal is to pretty-print ASTs corresponding to expressions.")
	print("    ctrl-d or ctrl-z to quit, depending on your operating system")

def consoleLoop():
	# Read/Parse/Print Loop
	parse = front_end.Parser().parse
	while True:
		try: text = promptedInput()
		except EOFError: break
		if text: display(parse(text))
		else: usage()
	

if __name__ == '__main__':
	usage()
	consoleLoop()
