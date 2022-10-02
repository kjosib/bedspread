"""
The obvious way to "test" the BVSM is to provide it with sample low-level programs
that represent the sorts of things I might expect to compile down to,
and then validate that the right answer comes out.
"""
import math
import unittest
from toys.simple_vm import Program, EntryPoint, SimpleMachine, ins_load_constant, ins_return, ins_primitive

class MyTestCase(unittest.TestCase):
	def test_literal(self):
		code = [(ins_load_constant, math.pi), (ins_return,)]
		entry_points = [EntryPoint(0, 0, 0),]
		p = Program(code, entry_points)
		sm = SimpleMachine(p)
		result = sm.fetch_execute_cycle(0)
		self.assertEqual(math.pi, result)
	
	def test_multiply(self):
		code = [
			(ins_load_constant, 3),
			(ins_load_constant, 5),
			(ins_primitive, "arith.mul"),
			(ins_return,),
		]
		entry_points = [EntryPoint(0, 0, 0),]
		p = Program(code, entry_points)
		sm = SimpleMachine(p)
		result = sm.fetch_execute_cycle(0)
		self.assertEqual(15, result)


if __name__ == '__main__':
	unittest.main()
