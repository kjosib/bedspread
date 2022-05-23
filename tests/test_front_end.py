import unittest
from bedspread import front_end, syntax


class Test_Parser(unittest.TestCase):
	
	def setUp(self) -> None:
		self.parse = front_end.Parser().parse
		
	def test_a_number(self):
		tree = self.parse("3.14159")
		self.assertIsInstance(tree, syntax.Literal)
		self.assertEqual(tree.value, 3.14159)
		
	def test_imaginary_number(self):
		tree = self.parse(" 5i ")
		self.assertIsInstance(tree, syntax.Literal)
		self.assertEqual(tree.value, 5j)

	def test_addition(self):
		tree = self.parse("57 + 23")
		self.assertIsInstance(tree, syntax.BinEx)
		self.assertEqual(tree.op.kind, '+')
		self.assertIsInstance(tree.lhs, syntax.Literal)
		self.assertIsInstance(tree.rhs, syntax.Literal)
		self.assertEqual(tree.lhs.span(), (0,2))
		self.assertEqual(tree.rhs.span(), (5,2))
		self.assertEqual(tree.lhs.value, 57)
		self.assertEqual(tree.rhs.value, 23)

	def test_conditional(self):
		tree = self.parse("{ when a+b>5 then Fred; when c=7 then Rodgers/Hammerstein; else Daphne }")
		self.assertIsInstance(tree, syntax.Switch)
		self.assertEqual(2, len(tree.cases))
		for case in tree.cases:
			self.assertIsInstance(case, syntax.Case)
		self.assertEqual(tree.cases[0].predicate.op.relation, 'GT')
		self.assertEqual(tree.cases[1].predicate.op.relation, 'EQ')
		self.assertIsInstance(tree.otherwise, syntax.Name)
		self.assertEqual(tree.otherwise.text, 'Daphne')
		
	def test_pemdas(self):
		for text in (
				"4 + 5 * 6",
				"4 * 5 + 6",
		):
			with self.subTest(text):
				tree = self.parse(text)
				self.assertIsInstance(tree, syntax.BinEx)
				self.assertEqual(tree.op.kind, '+') # Do the addition last; it's on the outside.
				
	def test_logical_not(self):
		tree = self.parse("not that")
		
	def test_logical_grouping(self):
		tree = self.parse("(this and not that) or the(other)")
		
	def test_apply_one(self):
		tree = self.parse("Fahrenheit(451)")
		self.assertIsInstance(tree, syntax.Apply)
		self.assertIsInstance(tree.function, syntax.Name)
		self.assertEqual(tree.function.text, 'Fahrenheit')
		self.assertIsInstance(tree.argument, syntax.Literal)
		self.assertEqual(tree.argument.value, 451)

	def test_apply_chain(self):
		tree = self.parse("a(1)(2)(b)")
		self.assertEqual(tree.argument.text, 'b')
		self.assertEqual(tree.function.argument.value, 2)
		self.assertEqual(tree.function.function.argument.value, 1)
		self.assertEqual(tree.function.function.function.text, 'a')

	def test_apply_two(self):
		tree = self.parse("point(x:3, y:5)")
		self.assertIsInstance(tree, syntax.Apply)
		self.assertIsInstance(tree.argument, dict)
		self.assertEqual({'x', 'y'}, tree.argument.keys())
		assert all(isinstance(node, syntax.Binding) for node in tree.argument.values())
		
	def test_double(self):
		tree = self.parse(r"\x[x+x](5)")
	
	# Error Cases
	
	def test_empty_string(self):
		tree = self.parse('')
		self.assertIsInstance(tree, syntax.Error)
		
	def test_excess(self):
		tree = self.parse('alpha bravo')
		self.assertIsInstance(tree, syntax.Error)
		

if __name__ == '__main__':
	unittest.main()
