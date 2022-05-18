import os
import unittest
from bedspread import front_end, syntax
from importlib import resources

class Test_Parser(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		front_end._refresh_grammar()
		
	def setUp(self) -> None:
		self.parse = front_end.Parser().parse
		
	def test_a_number(self):
		tree = self.parse("5")
		self.assertIsInstance(tree, syntax.Literal)

	def test_smoke(self):
		with self.subTest("addition"):
			tree = self.parse("57 + 23")
			self.assertIsInstance(tree, syntax.Arithmetic)
			self.assertEqual(tree.op.kind, '+')
			self.assertIsInstance(tree.lhs, syntax.Literal)
			self.assertIsInstance(tree.rhs, syntax.Literal)
			self.assertEqual(tree.lhs.span(), (0,2))
			self.assertEqual(tree.rhs.span(), (5,2))
			self.assertEqual(tree.lhs.value, 57)
			self.assertEqual(tree.rhs.value, 23)
			
		with self.subTest("conditional"):
			tree = self.parse("{ when a+b>5 then Fred; when c=7 then Rodgers/Hammerstein; else Daphne }")
			self.assertIsInstance(tree, syntax.Switch)
			self.assertEqual(2, len(tree.cases))
			for case in tree.cases:
				self.assertIsInstance(case, syntax.Case)
			self.assertEqual(tree.cases[0].predicate.op.relation, 'GT')
			self.assertEqual(tree.cases[1].predicate.op.relation, 'EQ')
			self.assertIsInstance(tree.otherwise, syntax.Name)
			self.assertEqual(tree.otherwise.text, 'Daphne')
		
		for text in (
				"4 + 5 * 6",
				"4 * 5 + 6",
		):
			with self.subTest(text):
				tree = self.parse(text)
				self.assertIsInstance(tree, syntax.Arithmetic)
				self.assertEqual(tree.op.kind, '+') # Do the addition last; it's on the outside.
				
	def test_errors(self):
		with self.subTest("empty string"):
			tree = self.parse('')
			self.assertIsInstance(tree, syntax.Error)

if __name__ == '__main__':
	unittest.main()
