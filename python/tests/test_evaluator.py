import unittest, math
from bedspread import front_end, evaluator, iform

parser = front_end.Parser()
scope = iform.AbstractScope()

def go(text):
	tree = parser.parse(text)
	plan = scope.convert(tree)
	return evaluator.eval(plan, scope)
	

class Test_Evaluator(unittest.TestCase):
	
	def test_literal(self):
		self.assertEqual(5, go("5"))
		self.assertEqual("abc", go('"abc"'))
		
	def test_arithmetic(self):
		self.assertEqual(25, go("3*3+4*4"))
		self.assertEqual(2, go("35 {mod} 3"))
		self.assertEqual("abcdef", go('"abc" + "def"'))

	def test_parens(self):
		self.assertEqual(12*7, go("3*(3+4)*4"))
		self.assertEqual(12*7, go("3*[3+4]*4"))

	def test_hypotenuse(self):
		self.assertIs(True, go("3*3 + 4*4 = 5*5"))
	
	def test_square(self):
		self.assertEqual(6.25, go(r"\x[x*x](2.5)"))
	
	def test_pythagoras(self):
		text = r"\a b[a^2+b^2](a:3,b:4)"
		self.assertEqual(25, go(text))
	
	def test_cond(self):
		self.assertEqual(14, go(r"when 1<2 then 14; when 3 > 2 then 42; else 12"))
		self.assertEqual(42, go(r"when 1>2 then 14; when 3 > 2 then 42; else 12"))
		self.assertEqual(12, go(r"when 1>2 then 14; when 3 < 2 then 42; else 12"))
		
	def test_math_is_integrated(self):
		self.assertEqual(math.tau, go('tau'))
		self.assertEqual(math.pi, go('4*atan(1)'))
		self.assertEqual(math.pi, go('4*atan2(x:1, y:1)'))
		self.assertEqual(math.pi, go('atan2(x:-1, y:0)'))

	def test_syntax_error_does_not_crash(self):
		self.assertIsInstance(go('5 6'), evaluator.Error)
		
	def test_zero_division_does_not_crash(self):
		self.assertIsInstance(go('1/0'), evaluator.Error)
		
	def test_domain_error(self):
		self.assertIsInstance(go('sqrt(-1)'), evaluator.Error)
		
	def test_partial_application(self):
		self.assertEqual(math.pi, go('atan2(x:-1)(y:0)'))
		
	def test_logcal_ops(self):
		self.assertIs( True, go('1>2 or not 1>2 and 5<7'))
		self.assertIs( True, go("1>2 xor 3<4"))
		
	def test_field_access(self):
		self.assertEqual("ABC", go('"abc".upper'))

if __name__ == '__main__':
	unittest.main()
