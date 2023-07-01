import sys
from importlib import resources
import json
from boozetools.macroparse import runtime
from boozetools.scanning.engine import IterableScanner
from bedspread import syntax

class Parser(runtime.TypicalApplication):
	RESERVED = {
		'AND' : syntax.Logical,
		'OR' : syntax.Logical,
		'XOR' : syntax.Logical,
		'EQV' : syntax.Logical,
		'NOT' : syntax.Operator,
		'WHEN': syntax.Operator,
		'THEN': syntax.Operator,
		'ELSE': syntax.Operator,
	}
	
	# TODO: This bad_token concept is hokey. BT should prefer an injectable on-error object.
	bad_token : syntax.Syntax = None
	
	def __init__(self):
		super().__init__(json.loads(resources.read_binary("bedspread", "grammar.automaton")))
	
	def scan_ignore(self, yy: IterableScanner, what_to_ignore): pass
	def scan_punctuation(self, yy: IterableScanner): syntax.Operator(yy, sys.intern(yy.match()))
	
	def scan_real(self, yy: IterableScanner): syntax.Literal(yy, float)
	def scan_imaginary(self, yy: IterableScanner): syntax.Literal(yy, lambda t :float(t[:-1])*1j)
	def scan_hexadecimal(self, yy: IterableScanner): syntax.Literal(yy, lambda t :int(yy.match(), 16))
	def scan_short_string(self, yy: IterableScanner): syntax.Literal(yy, lambda t: yy.match()[1:-1])
	
	scan_relop = syntax.RelOp
	
	def scan_word(self, yy: IterableScanner):
		upper = yy.match().upper()
		if upper in self.RESERVED:
			self.RESERVED[upper](yy, sys.intern(upper))
		else:
			syntax.Name(yy)
			
	def scan_token(self, yy: IterableScanner, kind):
		text = yy.match()
		yy.token(kind, text)
	
	parse_infix = syntax.Infix
	parse_prefix = syntax.Prefix
	parse_adverbial = syntax.Adverbial
	parse_case = syntax.Case
	parse_switch = syntax.Switch
	parse_error = syntax.Error
	parse_apply = syntax.Apply
	parse_apply_anaphor = syntax.ApplyAnaphor
	parse_bind_expression = syntax.BindExpression
	parse_bind_anaphor = syntax.BindAnaphor
	parse_parenthetical = syntax.Parenthetical
	parse_block = syntax.Block
	parse_field_access = syntax.FieldAccess
	parse_empty = syntax.EmptyList
	parse_list = syntax.ArrayExpression
	parse_dict = syntax.DictExpression
	
	def parse_abstraction(self, parameter, body):
		if isinstance(parameter, syntax.Error): return parameter
		elif isinstance(body, syntax.Error): return body
		else: return syntax.Abstraction(parameter, body)
	
	def parse_broken_apply(self, abstraction, argument):
		return syntax.Apply(abstraction, syntax.Error(argument))
	
	def parse_first_binding(self, binding:syntax.BindExpression):
		return {binding.name.text:binding}
	
	def parse_another_binding(self, some: dict[str:syntax.BindExpression], another:syntax.BindExpression):
		name = another.name.text
		if name in some:
			return syntax.Error(name, "already used earlier")
		else:
			some[name] = another
			return some
	
	def parse_first_case(self, item:syntax.Case):
		return [item]
	
	def parse_another_case(self, some:list[syntax.Case], another:syntax.Case):
		some.append(another)
		return some
	
	def parse_two_params(self, alpha:syntax.Name, bravo:syntax.Name):
		a, b = alpha.text, bravo.text
		if a == b: return syntax.Error(bravo, "already used earlier")
		else: return {a:alpha, b:bravo}
	
	def parse_another_param(self, some: dict[str: syntax.Name], another: syntax.Name):
		name = another.text
		if name in some:
			return syntax.Error(another, "already used earlier")
		else:
			some[name] = another
			return some
	
	def parse_first(self, item):
		return [item]
	
	def parse_more(self, them, item):
		them.append(item)
		return them
	
	def unexpected_token(self, symbol, semantic, pds):
		self.bad_token = semantic
	
	def unexpected_eof(self, pds):
		self.bad_token = syntax.Noise(self.yy.slice())
		
	def unexpected_character(self, yy: IterableScanner):
		yy.token("NOISE", syntax.Noise(yy.slice()))
		
	def will_recover(self, proposal):
		""" return an error token corresponding to the  """
		left = self.bad_token
		right = proposal[0][1] or syntax.Noise(self.yy.slice())
		return syntax.Noise(syntax.interval(left, right))