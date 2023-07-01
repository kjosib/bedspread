"""
This module aims to be the generic API for dealing with code-in-database issues.
Think of this as all support for deferred-execution mode.

Notes:

This implies that workspace.py is therefore also responsible for (what corresponds to) the symbol table.

The usual rule is that top-level clauses (functions, text, types)
are available in immediate mode, and to all other top-level functions.
Additionally, each clause can see its own subclauses, itself, and anything visible to its ancestors.
So, this means some concept of nested scopes is inevitable.

Because this is meant to be a structure that we can traverse in various ways,
it should also be possible to search it and/or generate a tree-view from it.

In the first version, the API probably works by reading and translating the entire database
into an intermediate form every time there's a change. The intermediate form needs to include
information about which definitions contain syntax errors. Later, static type checking can join.

One way to approach the visibility question is to simply follow static links.
"""
import sqlite3
from importlib import resources
from . import __version__, evaluator

help_message = """Bed Spread (version %s), interactive REPL
    Copyright 2022, by Ian Kjos
    Documentation is at http://bedspread.readthedocs.io
    License terms are at https://opensource.org/licenses/MIT
    Follow progress at https://github.com/kjosib/bedspread
    This is pre-alpha code. Current goal is a symbol table connected with some level of database integration.
    ctrl-d or ctrl-z to quit, depending on your operating system
    enter "help" to see this message again.""" % __version__

def create_sample_workspace():
	ws = Workspace(Connection(":memory:"))
	quadratic = ws.new_function("quadratic", ['a', 'b', 'c'], "[:root(-1), root(1):]", "Roots of a quadratic expression")
	quadratic.new_function("root", ['m'], "(-b + m*sqrt(b^2 - 4*a*c))/(2*a)", "One root; private to function 'quadratic'")
	ws.new_text("Gettysburg", resources.read_text("bedspread", "Gettysburg.txt",), 'Bliss copy. See https://www.abrahamlincolnonline.org/lincoln/speeches/gettysburg.htm for background.')
	ws.new_template('greet', ['who'], "", "Hello, {who}! Nice to meet you.")
	
class Workspace:
	def __init__(self, connection):
		pass
	
def _predefine(name, kind, parameters, body):
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
	cursor.execute("select * from symbol")
	for row in cursor:
		print(row['name'], ":", row['comment'])
		try: _predefine(row['name'], row['kind'], row['parameters'], row['body'])
		except evaluator.CannotCall as e: print("  -- The following parameters are unsuitable:", e.args[0])
	conn.close()

class Connection:
	def __init__(self, where):
		conn = sqlite3.connect(where, detect_types=sqlite3.PARSE_DECLTYPES)
		conn.row_factory = sqlite3.Row
		cursor = conn.cursor()
		cursor.execute("PRAGMA foreign_keys = ON", [])
		cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='version'")
		if not next(cursor)[0]:
			cursor.executescript(resources.read_text("bedspread", "schema.sql"))

def __init__():
	import math
	for name in dir(math):
		if name.startswith('_'): continue
		it = getattr(math, name)
		try: GLOBAL_SCOPE[name] = FFI(it) if callable(it) else it
		except CannotCall: pass

__init__()
