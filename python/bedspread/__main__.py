"""
For the moment, just a read-parse-print loop.

"""
import sqlite3
from importlib import resources
from bedspread import __version__, front_end, evaluator

parser = front_end.Parser()

def predefine(name, kind, parameters, body):
	ps = parameters.split() if parameters else []
	if kind == "text": item = body
	elif kind == "template": item = evaluator.Template(body)
	elif kind == "record": item = evaluator.RecordConstructor(name, ps)
	elif kind == "formula":
		body = parser.parse(body, filename=name)
		if len(ps) > 1: item = evaluator.UDF2(ps, body, evaluator.GLOBAL_SCOPE)
		elif len(ps) == 1: item = evaluator.UDF1(ps[0], body, evaluator.GLOBAL_SCOPE)
		else: item = evaluator.SemiConstant(body)
	else:
		print("Unknown symbol kind:", kind)
		return
	evaluator.GLOBAL_SCOPE[name] = item

def prepare():
	conn = sqlite3.connect("functions.bedspread", detect_types=sqlite3.PARSE_DECLTYPES)
	conn.row_factory = sqlite3.Row
	cursor = conn.cursor()
	cursor.execute("PRAGMA foreign_keys = ON", [])
	cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='version'")
	if not next(cursor)[0]:
		cursor.executescript(resources.read_text("bedspread", "schema.sql"))
	cursor.execute("select * from symbol")
	for row in cursor:
		print(row['name'], ":", row['comment'])
		try: predefine(row['name'], row['kind'], row['parameters'], row['body'])
		except evaluator.CannotCall as e: print("  -- The following parameters are unsuitable:", e.args[0])
	conn.close()

def consoleLoop():
	# Read/Parse/Print Loop
	usage = evaluator.evaluate(parser.parse('help'))
	print(usage)
	while True:
		try: text = input("Ready >> ")
		except EOFError: break
		if text:
			tree = parser.parse(text)
			value = evaluator.evaluate(tree)
			if isinstance(value, evaluator.Error):
				# FIXME: This is now wrong if the error is detected while evaluating pre-parsed code.
				#  If the error object stored which function created it, then we could look that up in a symbol table.
				#  One way to get there is a slightly more sophisticated scope-and-environment model,
				#  which will be necessary anyway soon. (Maybe static and dynamic links are on the heap?)
				parser.source.complain(*value.exp.span())
			print(value)
		else: print("I beg your pardon?")
	

if __name__ == '__main__':
	prepare()
	consoleLoop()
