import sys
from importlib import resources
import json
from boozetools.support import runtime, interfaces
from bedspread import syntax

def _refresh_grammar():
	import os
	from boozetools.macroparse.compiler import compile_file
	
	if resources.is_resource("bedspread", "grammar.md"):
		with resources.path("bedspread", "grammar.md") as src:
			with resources.path("bedspread", "grammar.automaton") as dst:
				if (not os.path.exists(dst)) or (os.stat(dst).st_mtime < os.stat(src).st_mtime):
					with open(dst, 'w') as ofh:
						json.dump(
							compile_file(src, method='LR1'),
							ofh,
							separators=(',', ':'),
							sort_keys=True,
						)


class Parser(runtime.TypicalApplication):
	RESERVED = {
		'AND' : syntax.Logical,
		'OR' : syntax.Logical,
		'XOR' : syntax.Logical,
		'EQV' : syntax.Logical,
		'IMP' : syntax.Logical,
		'AS': syntax.Operator,
		'WHEN': syntax.Operator,
		'THEN': syntax.Operator,
		'ELSE': syntax.Operator,
	}
	
	def __init__(self):
		super().__init__(json.loads(resources.read_binary("bedspread", "grammar.automaton")))
		
	def scan_ignore(self, yy: interfaces.Scanner, what_to_ignore): pass
	
	def scan_punctuation(self, yy: interfaces.Scanner): syntax.Operator(yy, sys.intern(yy.matched_text()))
	
	scan_relop = syntax.RelOp
	
	def scan_real(self, yy: interfaces.Scanner): syntax.Literal(yy, float)
	
	def scan_imaginary(self, yy: interfaces.Scanner): syntax.Literal(yy, lambda t :float(t[:- 1 *1j]))
	
	def scan_hexadecimal(self, yy: interfaces.Scanner): syntax.Literal(yy, lambda t :int(yy.matched_text(), 16))
	
	def scan_word(self, yy: interfaces.Scanner):
		upper = yy.matched_text().upper()
		if upper in self.RESERVED:
			self.RESERVED[upper](yy, sys.intern(upper))
		else:
			syntax.Name(yy)
			
	def scan_token(self, yy: interfaces.Scanner, kind):
		text = yy.matched_text()
		yy.token(kind, text)
	
	parse_arithmetic = syntax.Arithmetic
	parse_relation = syntax.Relation
	parse_case = syntax.Case
	parse_switch = syntax.Switch
	parse_error = syntax.Error
	
	def parse_first_case(self, case:syntax.Case):
		return [case]
	
	def parse_another_case(self, cases:list[syntax.Case], case:syntax.Case):
		cases.append(case)
		return cases
	
