"""
The old evaluator ran on syntax forms directly. That's inflexible and troublesome.
The new evaluator will run an intermediate form which determines (bare) name bindings in advance.
"""

from collections import ChainMap, namedtuple
import inspect
from . import iform, syntax
from string import Formatter

class CannotCall(Exception):
	""" Internal exception meaning the FFI binding did not work. """
	pass

class Error:
	""" A kind of value which means there is some error. """
	def __init__(self, exp:syntax.Syntax, problem:str):
		self.exp = exp
		self.problem = problem
	def __str__(self):
		return "<<Error: %s %s>>"%(self.exp.slice(), self.problem)

class Function:
	""" A kind of value that can be applied to create new values """
	def has_parameter(self, name:str) -> bool:
		raise NotImplementedError(type(self))

	def eval(self, arg, caller_env):
		""" arg is caller syntax and env is the caller's scope. """
		raise NotImplementedError(type(self))

	def eval_anaphor(self, tree:syntax.ApplyAnaphor, caller_env):
		""" tree is caller syntax and env is the caller's scope. """
		raise NotImplementedError(type(self))

class MultaryFunction(Function):
	def __init__(self, parameter_names):
		self.parameter_names = set(parameter_names)
		bogons = [p for p in self.parameter_names if not p.isidentifier()]
		if bogons: raise CannotCall(bogons)

	def has_parameter(self, name: str) -> bool:
		return name in self.parameter_names
	
	def __bad_call(self, arg):
		return Error(arg, "Multi-parameter function expects named arguments %r" % self.parameter_names)

	def eval(self, arg, caller_env):
		if isinstance(arg, dict):
			extra = arg.keys() - self.parameter_names
			if extra: return self.__bad_call(arg[extra.pop()])
			free = self.parameter_names - arg.keys()
			bound = {}
			for k, v in arg.items():
				value = eval(v.argument, caller_env)
				if isinstance(value, Error): return value
				bound[k] = value
			if free: return PartialFunction(self, bound, free)
			return self.raw_multi(bound)
		elif len(self.parameter_names) == 1:
			value = eval(arg, caller_env)
			if isinstance(value, Error): return value
			else: return self.raw_multi({next(iter(self.parameter_names)):value})
		else:
			return self.__bad_call(arg)

	def raw_multi(self, bound:dict[str:object]):
		raise NotImplementedError(type(self))
	
	def eval_anaphor(self, tree:syntax.ApplyAnaphor, caller_env):
		bound = {}
		free = set()
		for p in self.parameter_names:
			try: bound[p] = caller_env[p]
			except KeyError: free.add(p)
		if free and bound: return PartialFunction(self, bound, free)
		elif bound: return self.raw_multi(bound)
		else: return self.__bad_call(tree)

class RecordConstructor(MultaryFunction):
	def __init__(self, name, parameter_names):
		super().__init__(parameter_names)
		self.name = name
		self.type = namedtuple(name, parameter_names)
	
	def raw_multi(self, bound:dict[str:object]):
		return self.type(**bound)

class PartialFunction(MultaryFunction):
	def __init__(self, basis:MultaryFunction, bound:dict, free:set):
		self.basis = basis
		self.bound = bound
		super().__init__(free)
	
	def raw_multi(self, bound:dict[str:object]):
		return self.basis.raw_multi({**self.bound, **bound})

class UnaryFunction(Function):
	def has_parameter(self, name: str) -> bool:
		return False

	def eval(self, arg, caller_env):
		if isinstance(arg, dict):
			first_arg = next(iter(arg.values()))
			return Error(first_arg, "Unary Function expects a single unadorned argument.")
		else:
			value = eval(arg, caller_env)
			if isinstance(value, Error): return value
			return self.raw_single(value)

	def raw_single(self, value:object):
		raise NotImplementedError(type(self))
	

class PythonUnary(UnaryFunction):
	def __init__(self, fn):
		self.raw_single = fn
		
	def eval_anaphor(self, tree:syntax.ApplyAnaphor, caller_env):
		return Error(tree, "This built-in function takes only one anonymous argument, so the @ here is confusing.")


class PythonMultary(MultaryFunction):
	def __init__(self, fn, params):
		super().__init__(params)
		self.__fn = fn
		self.param_order = tuple(params)
	
	def raw_multi(self, bound:dict[str:object]):
		return self.__fn(*(bound[k] for k in self.param_order))

class Template(MultaryFunction):
	__formatter = Formatter()
	def __init__(self, text):
		params = [x[1] for x in self.__formatter.parse(text) if x[1]]
		super().__init__(params)
		self.text = text
	
	def raw_multi(self, bound: dict[str:object]):
		return self.text.format(**bound)


class UDF1(UnaryFunction):
	def __init__(self, parameter, body, env):
		self.parameter = parameter
		self.body = body
		self.lexical_scope = env
		
	def raw_single(self, value:object):
		activation_env = ChainMap({self.parameter: value}, self.lexical_scope)
		return eval(self.body, activation_env)
	
	def eval_anaphor(self, tree:syntax.ApplyAnaphor, caller_env):
		try: value = caller_env[self.parameter]
		except AttributeError: return Error(tree, "This user-defined function's argument is called %r, but there is no such name in the caller's environment."%self.parameter)
		else: return self.raw_single(value)
	
class UDF2(MultaryFunction):
	def __init__(self, parameter_names, body:syntax.Expression, env):
		super().__init__(parameter_names)
		self.body = body
		self.lexical_scope = env
	
	def raw_multi(self, bound: dict[str:object]):
		activation_env = ChainMap(bound, self.lexical_scope)
		return eval(self.body, activation_env)


def eval(tree:syntax.Expression, env):
	"""
	The static scope tells how to look up definitions.
	The dynamic scope tells how to look up bindings.
	For purpose of baby-steps interpretation, look up names in the dynamic scope first;
	if that fails, look them up in the static scope. But we establish a rule that
	"""
	# Converts SYNTAX to VALUE
	if isinstance(tree, syntax.Literal):
		return tree.value
	elif isinstance(tree, syntax.Name):
		try: value = env[tree.text]
		except KeyError: return Error(tree, "No such name in scope.")
		return value
	elif isinstance(tree, syntax.Infix):
		lhs = eval(tree.lhs, env)
		if isinstance(lhs, Error):
			return lhs
		else:
			rhs = eval(tree.rhs, env)
			if isinstance(rhs, Error):
				return rhs
			else:
				primitive = PRIMITIVE_BINARY[_select_primitive(tree.op)]
				try: return primitive(lhs, rhs)
				except Exception as e: return Error(tree, repr(e))
	elif isinstance(tree, syntax.Prefix):
		operand = eval(tree.exp, env)
		if isinstance(operand, Error):
			return operand
		else:
			return PRIMITIVE_UNARY[tree.op.kind](operand)
	elif isinstance(tree, syntax.Parenthetical):
		return eval(tree.exp, env)
	elif isinstance(tree, syntax.Block):
		return eval(tree.exp, env)
	elif isinstance(tree, syntax.Apply):
		function = eval(tree.function, env)
		if isinstance(function, Error): return function
		elif isinstance(function, Function):
			try: return function.eval(tree.argument, env)
			except Exception as e: return Error(tree, repr(e))
		else: return Error(tree.function, "This is not a function. I can't invoke it with parameters.")
	elif isinstance(tree, syntax.Abstraction):
		if isinstance(tree.parameter, syntax.Name):
			return UDF1(tree.parameter.text, tree.body, env)
		elif isinstance(tree.parameter, dict):
			return UDF2(tree.parameter.keys(), tree.body, env)
		else:
			raise RuntimeError("This can't happen.")
	elif isinstance(tree, syntax.Switch):
		for case in tree.cases:
			test = eval(case.predicate, env)
			if test is True: return eval(case.consequence, env)
			elif test is not False: return Error(case.predicate, "did not evaluate as a Boolean predicate")
		else:
			return eval(tree.otherwise, env)
	elif isinstance(tree, syntax.Error):
		return Error(tree, "Syntax Error")
	elif isinstance(tree, syntax.FieldAccess):
		lhs = eval(tree.exp, env)
		if isinstance(lhs, Error): return lhs
		try: item = getattr(lhs, tree.name.text)
		except AttributeError as ae: return Error(tree, str(ae))
		if callable(item): item = FFI(item)
		return item
	elif isinstance(tree, syntax.ApplyAnaphor):
		fn = eval(tree.function, env)
		if isinstance(fn, Function):
			return fn.eval_anaphor(tree, env)
		else:
			return Error(tree, "This is not a function. I can't invoke it with parameters.")
	raise RuntimeError("Incomplete Evaluator: ", tree)

### Here's the part that pre-loads some global functions to play with:
def FFI(it):
	try: signature = inspect.signature(it)
	except ValueError: raise CannotCall(it)
	if len(signature.parameters) == 1:
		return PythonUnary(it)
	elif not signature.parameters:
		return it()
	elif all(len(k)==1 for k in signature.parameters.keys()):
		return PythonMultary(it, signature.parameters.keys())
