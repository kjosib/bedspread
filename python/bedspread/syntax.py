"""
Syntax Tree Components
This is probably going to end up object-oriented for now.
Bollox.
"""
from pprint import pprint


class Syntax:
	def span(self) -> tuple[int, int]:
		raise NotImplementedError(type(self))

def _interval(a,b) -> tuple[int, int]:
	""" For composing spans """
	return a.span()[0], b.span()[1]

class Operator(Syntax):
	_span : tuple[int, int]
	
	def __init__(self, yy, kind):
		self._span = yy.current_span()
		self.kind = kind
		yy.token(kind, self)
	
	def span(self):
		return self._span
	
	def excerpt(self, text):
		left, count = self._span
		return text[left:left + count]
	
	pass

class Atom(Operator):
	def __init__(self, yy, kind):
		super().__init__(yy, kind)
		self.text = yy.matched_text()

class Name(Atom):
	def __init__(self, yy):
		super().__init__(yy, "NAME")

class Literal(Atom):
	def __init__(self, yy, read):
		super().__init__(yy, "LITERAL")
		self.value = read(self.text)
	pass

class RelOp(Operator):
	CANONICAL = {
		'EQ':'==',
		'NE':'!=',
		'LT':'<',
		'LE':'<=',
		'GT':'>',
		'GE':'>=',
	}
	def __init__(self, yy, relation):
		super().__init__(yy, "RELOP")
		self.text = self.CANONICAL[relation]
		self.relation = relation
	def __str__(self):
		return self.CANONICAL[self.relation]

class Logical(Operator):
	def __init__(self, yy, logic):
		super().__init__(yy, "LOGIC")
		self.logic = logic
	pass

class Expression(Syntax):
	pass

class Error(Expression):
	def __init__(self, *args):
		pprint(args)
		self.args = args

class Arithmetic(Expression):
	def __init__(self, lhs:Expression, op:Operator, rhs:Expression):
		self.lhs = lhs
		self.op = op
		self.rhs = rhs
	
	def span(self) -> tuple[int, int]:
		return _interval(self.lhs, self.rhs)
	
	def __str__(self):
		return "[Arithmetic: %s %s %s]"%(self.lhs, self.op, self.rhs)

class Relation(Expression):
	def __init__(self, lhs:Expression, op:RelOp, rhs:Expression):
		self.lhs = lhs
		self.op = op
		self.rhs = rhs
	
	def __str__(self):
		return "[Relation: %s %s %s]"%(self.lhs, self.op, self.rhs)

class Case(Expression):
	def __init__(self, predicate, consequence):
		self.predicate = predicate
		self.consequence = consequence
		
class Switch(Expression):
	def __init__(self, cases:list[Case], otherwise:Expression):
		self.cases = cases
		self.otherwise = otherwise
