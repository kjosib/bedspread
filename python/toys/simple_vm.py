"""
Simple Virtual Machine

This was written to play around with some kind of fetch-execute cycle with minimal ceremony.
I wanted to try a few ideas for implementing the semantics operationally.
Something along these lines (but not this exactly) might eventually provide a road map to
building a code generator.

Possible "instructions" to add:
* Computed-goto a.k.a. switch dispatch, useful for type-case matching.
* Construct Data Object -- presumably from fields on the stack.
* Extract field from data object.

"""

import operator
from typing import Optional, NamedTuple, Any
from dataclasses import dataclass

class EntryPoint(NamedTuple):
	ip: int
	arity: int
	static_depth: int

class Program(NamedTuple):
	code: list
	entry_points: list[EntryPoint]

@dataclass
class ActivationRecord:
	""" Corresponding to the principle registers of the machine. """
	ip: int
	dynamic_link: Optional["ActivationRecord"]
	static_link: Optional["ActivationRecord"]
	stack: list
	static_depth: int

class Thunk(NamedTuple):
	# These are more like call-by-name thunks than call-by-need thunks.
	index: int
	static_link: ActivationRecord

class SimpleMachine:
	program: Program
	ar: Optional[ActivationRecord]
	result: Any
	
	def __init__(self, program:Program):
		self.program = program
		self.ar = None
		self.result = None
	
	def take(self, arity) -> list:
		s=self.ar.stack
		if arity:
			args = s[-arity:]
			del s[-arity:]
			return args
		else:
			return []
	
	def push(self, item):
		self.ar.stack.append(item)
	
	def pop1(self):
		return self.ar.stack.pop()
	
	def static(self, steps:int) -> ActivationRecord:
		ar = self.ar
		for _ in range(steps):
			ar = ar.static_link
		return ar
	
	def fetch_execute_cycle(self, index, *args):
		"""
		Probably the most concise way to make an instruction dispatcher in Python is
		if the instructions themselves are just procedures that mutate machine state.
		Rather, they should be a pair consisting of a reference to such a procedure
		followed by a tuple of additional arguments thereto.
		"""
		entry = self.program.entry_points[index]
		if entry.static_depth != 0:
			raise ValueError("Tried to use nested function as main function.")
		if entry.arity != len(args):
			raise TypeError("Expected %d varargs, got %d"%(entry.arity, len(args)))
		self.ar = ActivationRecord(entry.ip, None, None, list(args), entry.static_depth)
		while self.ar is not None:
			(ins, *args) = self.program.code[self.ar.ip]
			self.ar.ip += 1
			ins(self, *args)
		return self.result

def ins_load_constant(m:SimpleMachine, datum:Any):
	m.push(datum)

def ins_load_local(m:SimpleMachine, index:int):
	m.push(m.ar.stack[index])

def ins_load_nonlocal(m:SimpleMachine, steps:int, index:int):
	m.push(m.static(steps).stack[index])

def ins_primitive(m:SimpleMachine, name):
	impl, arity = PRIMITIVES[name]
	result = impl(*m.take(arity))
	m.push(result)

def ins_apply(m:SimpleMachine):
	thunk:Thunk = m.pop1()
	entry = m.program.entry_points[thunk.index]
	args = m.take(entry.arity)
	m.ar = ActivationRecord(entry.ip, m.ar, thunk.static_link, args, entry.static_depth)

def ins_bind(m:SimpleMachine, index:int):
	# which means that partial-applications could be implemented as ordinary lexically-nested definitions.
	# There's no concern for binding in the Pythonic sense because there are no loops; only tail-calls.
	# Similarly lambda abstraction just creates a lexically-nested entry point.
	entry = m.program.entry_points[index]
	steps = m.ar.static_depth + 1 - entry.static_depth
	m.push(Thunk(index, m.static(steps)))

def ins_call(m:SimpleMachine, index:int):
	# This is just the combination of a bind and apply in one step.
	entry = m.program.entry_points[index]
	steps = m.ar.static_depth + 1 - entry.static_depth
	args = m.take(entry.arity)
	m.ar = ActivationRecord(entry.ip, m.ar, m.static(steps), args, entry.static_depth)

def ins_return(m:SimpleMachine):
	result = m.pop1()
	m.ar = m.ar.dynamic_link
	if m.ar is None:
		m.result = result
	else:
		m.ar.stack.append(result)

def ins_tail_call(m:SimpleMachine, index:int):
	entry = m.program.entry_points[index]
	args = m.take(entry.arity)
	steps = m.ar.static_depth + 1 - entry.static_depth
	m.ar = ActivationRecord(entry.ip, m.ar.dynamic_link, m.static(steps), args, entry.static_depth)

def ins_branch(m:SimpleMachine, ip:int):
	m.ar.ip = ip

def ins_cond(m:SimpleMachine, if_true:int, if_false:int):
	m.ar.ip = if_true if m.pop1() else if_false

def ins_read_field(m:SimpleMachine, index:int):
	m.push(m.pop1()[index])

def ins_dynamic_index(m:SimpleMachine):
	ins_read_field(m, m.pop1())


PRIMITIVES = {
	"arith.neg": (operator.neg, 1),
	"arith.add": (operator.add, 2),
	"arith.sub": (operator.sub, 2),
	"arith.mul": (operator.mul, 2),
	"arith.div": (operator.truediv, 2),
	"arith.mod": (operator.mod, 2),
	"arith.pow": (operator.pow, 2),
	
	"relop.eq": (operator.eq, 2),
	"relop.ne": (operator.ne, 2),
	"relop.lt": (operator.lt, 2),
	"relop.le": (operator.le, 2),
	"relop.ge": (operator.ge, 2),
	"relop.gt": (operator.gt, 2),
	
	"logic.not": (operator.not_, 1),
	"logic.or": (operator.or_, 2),
	"logic.and": (operator.and_, 2),
	'logic.xor': (operator.xor, 2),
	'logic.eqv': (operator.is_, 2),  # Hack, but works in context: True and False are singletons in Python's runtime.
}

