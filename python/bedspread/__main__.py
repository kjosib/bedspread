"""
For the moment, just a read-parse-print loop.

"""
import sys
from bedspread import front_end, evaluator, workspace

parser = front_end.Parser()

def consoleLoop(ws):
	# Read/Parse/Eval/Print Loop
	print(workspace.help_message)
	while True:
		try: text = input("Ready >> ")
		except EOFError: break
		if text:
			parser.bad_token = None
			tree = parser.parse(text)
			if parser.bad_token is None:
				value = evaluator.evaluate(tree)
				if isinstance(value, evaluator.Error):
					# Then an evaluator.Error will need a debug pointer.
					# *value.exp.span()
					print("To do: Properly connect runtime errors to source locations.", file=sys.stderr)
				print(value)
			else:
				parser.source.complain(*parser.bad_token.span(), message="I got confused. Typo?")
		else: print("I beg your pardon?")
	

if __name__ == '__main__':
	connection = workspace.Connection("functions.bedspread")
	ws = workspace.Workspace(connection)
	consoleLoop(ws)
