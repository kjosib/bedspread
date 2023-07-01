"""
Call-By-Need with Direct Interpretation
Absolutely simplest, most straight-forward possible implementation.

Functions (closures and primitive) are now values in the usual sense,
so that passing them around works in the usual way,
and higher-order functions should do all the right things.

Evaluation is lazy and theoretically memoized, although nothing prevents
a function from being evaluated twice with equivalent arguments
that come from different places.

This has no concept of compound data. In principle you could do it
with procedures a'la SICP, but in practice that's ugly and verbose.
Are constructors and accessors enough? Sort of.
One also needs a way to translate declarations into constructors,
and to deal well with the notion of lazy data.
In some languages all data is lazy.
In others, maybe some fields are strict.

Last, it's probably worth considering a strictness algebra.
If some parameter is bound to be forced, then it may as well be strict.
This changes the efficiency of computing that parameter.

"""
from typing import NamedTuple, Any
import abc
import inspect

class Environment(abc.ABC):
	@abc.abstractmethod
	def resolve(self, name:str) -> Any:
		pass

class Expr(abc.ABC):
	@abc.abstractmethod
	def evaluate(self, env:Environment) -> Any:
		pass

class Procedure(abc.ABC):
	""" A special kind of value which can be applied. """
	
	@abc.abstractmethod
	def apply(self, env:Environment, args:list[Expr]) -> Any:
		""" Application is to expressions, thus supporting call-by-whatever. """

ABSENT = object()
class Thunk:
	""" A special not-yet-value which can be forced. """
	def __init__(self, env: Environment, expr: Expr):
		self._env = env
		self._expr = expr
		self._value = ABSENT
		
	def force(self):
		if self._value is ABSENT:
			self._value = actual_value(self._expr.evaluate(self._env))
			del self._env
		return self._value

def actual_value(it):
	while isinstance(it, Thunk):
		it = it.force()
	return it

class EntryPoint(NamedTuple):
	""" The static syntactical representation of something that might be closed over. """
	params: list[str]
	expression: Expr
	children: dict[str: "EntryPoint"]
	name: str

	def execute(self, static_link:"Environment", args:list[Thunk]):
		if len(args) != len(self.params):
			raise TypeError("Wrong number of arguments")
		bindings = dict(zip(self.params, args))
		env = InnerEnv(self.children, bindings, static_link)
		return self.expression.evaluate(env)


class NullEnv(Environment):
	""" Effectively the built-in scope, but with nothing built in. (Yet?) """
	def resolve(self, name:str) -> Any:
		raise RuntimeError("unknown: " + repr(name))
null_env = NullEnv()

class InnerEnv(Environment):
	def __init__(self, children:dict[str: EntryPoint], bindings:dict[str:Any], static_link:Environment):
		self._children = children
		self._bindings = bindings
		self._static_link = static_link
	
	def resolve(self, name) -> Any:
		if name in self._bindings:
			return self._bindings[name]
		elif name in self._children:
			entry = self._children[name]
			closure = Closure(entry, self)
			self._bindings[name] = closure
			return closure
		else:
			return self._static_link.resolve(name)


class Closure(Procedure):
	""" The run-time manifestation of a LambdaAbstraction, which incidentally is a kind of value. """
	# Incidentally, named children can be done by putting corresponding closures in the local environment.
	# Also, thunks are closely related. They take an expression, not an entry point, though.
	
	entry: EntryPoint
	static_link: "Environment"

	def __init__(self, entry:EntryPoint, static_link:"Environment"):
		self.entry = entry
		self.static_link = static_link

	def apply(self, env:"Environment", args:list[Expr]) -> Any:
		arity = len(self.entry.params)
		if arity != len(args):
			raise TypeError("Procedure %s expected %d args, got %d."%(self.entry.name, arity, len(args)))
		thunks = [Thunk(env, a) for a in args]
		return self.entry.execute(self.static_link, thunks)


class Primitive(Procedure):
	""" All parameters to primitive procedures are strict. Also a kind of value, like a closure. """
	def __init__(self, op):
		assert callable(op)
		signature = inspect.signature(op)
		self.op = op
		self.params = list(signature.parameters.keys())
		
	def apply(self, env:"Environment", args:list[Expr]) -> Any:
		if len(self.params) != len(args):
			raise TypeError("Native procedure %s expected %d args, got %d."%(self.op, len(self.params), len(args)))
		values = [actual_value(a.evaluate(env)) for a in args]
		return self.op(*values)


#############################

class Constant(Expr):
	__slots__ = ("_value",)
	def __init__(self, value):
		self._value = value
		
	def evaluate(self, env):
		return self._value

class Name(Expr):
	__slots__ = ("name",)
	def __init__(self, name):
		self.name = name
	def evaluate(self, env):
		return env.resolve(self.name)

class Call(Expr):
	__slots__ = ("fn_exp", "args")
	def __init__(self, fn_exp, *args):
		# At some point I'll have to make the type-judgment that fn_exp is a procedure of suitable arity.
		assert isinstance(fn_exp, Expr), fn_exp
		assert all(isinstance(a, Expr) for a in args)
		self.fn_exp = fn_exp
		self.args = args
	def evaluate(self, env):
		procedure = self.fn_exp.evaluate(env)
		return procedure.apply(env, self.args)

class If(Expr):
	predicate: Expr
	consequent: Expr
	alternative: Expr
	
	def __init__(self, predicate:Expr, consequent:Expr, alternative:Expr):
		self.predicate = predicate
		self.consequent = consequent
		self.alternative = alternative
		
	def evaluate(self, env):
		if actual_value(self.predicate.evaluate(env)):
			return self.consequent.evaluate(env)
		else:
			return self.alternative.evaluate(env)
		
