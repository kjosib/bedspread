from toys.call_by_need import (
	EntryPoint, InnerEnv, Primitive, Constant, Name, Call, If,
	Closure, null_env, actual_value
)
import operator

import unittest

class MyTestCase(unittest.TestCase):
	def test_smoke(self):
		c = Constant(3)
		ep = EntryPoint([], c, {}, "smoke")
		env = InnerEnv(ep.children, {}, null_env)
		assert ep.expression.evaluate(env) == 3
	
	def test_primitive(self):
		one = Constant(1)
		le = Constant(Primitive(operator.le))
		predicate = Call(le, Name("x"), one)
		assert False is predicate.evaluate(InnerEnv({}, {"x": 4}, null_env))
		assert True is predicate.evaluate(InnerEnv({}, {"x": 0}, null_env))

	def test_udf_call(self):
		plus = Constant(Primitive(operator.add))
		ep = EntryPoint(["a"], Call(plus, Name("a"), Name("a")), {}, "twice")
		closure = Closure(ep, null_env) # This is a value I can apply...
		fourteen = closure.apply(null_env, [Constant(7)])
		self.assertEqual(14, fourteen)
		
	def test_factorial(self):
		one = Constant(1)
		le = Constant(Primitive(operator.le))
		x = Name("x")
		predicate = Call(le, Name("x"), one)
		fact = Name("fact")
		mul = Constant(Primitive(operator.mul))
		sub = Constant(Primitive(operator.sub))
		fact_expr = If(predicate, one, Call(mul, x, Call(fact, Call(sub, x, one))))
		fact_ep = EntryPoint(["x"], fact_expr, {}, "fact")
		expression = Call(fact, Constant(4))
		env = InnerEnv({"fact":fact_ep}, {}, null_env)
		self.assertEqual(24, expression.evaluate(env))
		
	def test_laziness(self):
		zero_division = Call(Constant(Primitive(operator.truediv)), Constant(1), Constant(0))
		predicate = Call(Constant(Primitive(operator.eq)), Name('a'), Constant(0))
		cond = If(predicate, Constant(1), Name('b'))
		attempt_ep = EntryPoint(['a', 'b'], cond, {}, 'attempt')
		env = InnerEnv({"try":attempt_ep}, {}, null_env)
		self.assertEqual(1, actual_value(Call(Name("try"), Constant(0), zero_division).evaluate(env)))
		with self.assertRaises(ZeroDivisionError):
			actual_value(Call(Name("try"), Constant(1), zero_division).evaluate(env))
		

if __name__ == '__main__':
	unittest.main()
