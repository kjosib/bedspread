import sys
from importlib import resources
import json
from boozetools.support import runtime, interfaces
from bedspread import syntax

class Parser(runtime.TypicalApplication):
	RESERVED = {
		'AND' : syntax.Logical,
		'OR' : syntax.Logical,
		'XOR' : syntax.Logical,
		'EQV' : syntax.Logical,
		'IMP' : syntax.Logical,
		'NOT' : syntax.Operator,
		'AS': syntax.Operator,
		'WHEN': syntax.Operator,
		'THEN': syntax.Operator,
		'ELSE': syntax.Operator,
	}
	__confusing_token : syntax.Syntax = None
	def __init__(self):
		super().__init__(json.loads(resources.read_binary("bedspread", "grammar.automaton")))
	
	def scan_ignore(self, yy: interfaces.Scanner, what_to_ignore): pass
	def scan_punctuation(self, yy: interfaces.Scanner): syntax.Operator(yy, sys.intern(yy.matched_text()))
	
	def scan_real(self, yy: interfaces.Scanner): syntax.Literal(yy, float)
	def scan_imaginary(self, yy: interfaces.Scanner): syntax.Literal(yy, lambda t :float(t[:-1])*1j)
	def scan_hexadecimal(self, yy: interfaces.Scanner): syntax.Literal(yy, lambda t :int(yy.matched_text(), 16))
	
	scan_relop = syntax.RelOp
	
	def scan_word(self, yy: interfaces.Scanner):
		upper = yy.matched_text().upper()
		if upper in self.RESERVED:
			self.RESERVED[upper](yy, sys.intern(upper))
		else:
			syntax.Name(yy)
			
	def scan_token(self, yy: interfaces.Scanner, kind):
		text = yy.matched_text()
		yy.token(kind, text)
	
	parse_binary_operation = syntax.BinEx
	parse_case = syntax.Case
	parse_switch = syntax.Switch
	parse_unary = syntax.Unary
	parse_error = syntax.Error
	parse_apply = syntax.Apply
	parse_abstraction = syntax.Abstract
	parse_bind = syntax.Bind
	parse_parenthetical = syntax.Parenthetical
	parse_block = syntax.Block
	
	def parse_broken_apply(self, abstraction, argument):
		return syntax.Apply(abstraction, syntax.Error(argument))
	
	def parse_first(self, item:syntax.Syntax):
		return [item]
	
	def parse_another(self, some:list[syntax.Syntax], another:syntax.Syntax):
		some.append(another)
		return some
	
	def parse_two_names(self, alpha, bravo):
		return [alpha, bravo]
	
	def unexpected_token(self, symbol, semantic, pds):
		self.__confusing_token = semantic
	
	def unexpected_eof(self, pds):
		self.__confusing_token = syntax.Noise(self.yy.current_span())
		
	def unexpected_character(self, yy: interfaces.Scanner):
		yy.token("NOISE", syntax.Noise(yy.current_span()))
		
	def will_recover(self, proposal):
		""" return an error token corresponding to the  """
		left = self.__confusing_token
		right = proposal[0][1] or syntax.Noise(self.yy.current_span())
		return syntax.Noise(syntax.interval(left, right))