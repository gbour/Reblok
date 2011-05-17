#!/usr/bin/python
# -*- coding: utf8 -*-
import unittest
from reblok import Parser, namespaces as ns, opcodes as op

class TestReblokBasics(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		unittest.TestCase.__init__(self, *args, **kwargs)
		self.parser = Parser()

	def walk(code):
		return self.parser.walk(code)

	def test_01arithmetic(self):
		tree = self.parser.walk(lambda u: u + 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.ADD, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u - 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.SUB, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u * 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.MUL, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u / 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.DIV, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u % 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.MOD, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])
	
	def test_02cmp(self):
		tree = self.parser.walk(lambda u: u == 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA, [
				[op.RET,
					(op.EQ,
						(op.VAR  , 'u', ns.LOCAL),
						(op.CONST, 5)
				)]],
				[('u', op.UNDEF)], None, None, [], {}]
		)

		tree = self.parser.walk(lambda u: u != 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.NEQ, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		# <> and != are same operator
		tree = self.parser.walk(lambda u: u <> 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.NEQ, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u > 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.GT, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u < 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.LT, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u >= 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.GEQ, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u <= 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.LEQ, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u is 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.ID, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u is not 5)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.NID, (op.VAR, 'u', ns.LOCAL), (op.CONST , 5))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

	def test_03bool(self):
		tree = self.parser.walk(lambda u: u or True)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.OR, (op.VAR, 'u', ns.LOCAL), (op.CONST , True)]]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: True or u)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.OR, (op.CONST , True), (op.VAR, 'u', ns.LOCAL)]]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u and True)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.AND, (op.VAR, 'u', ns.LOCAL), (op.CONST , True)]]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: True and u)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.AND, (op.CONST , True), (op.VAR, 'u', ns.LOCAL)]]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: not u)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.NOT, (op.VAR, 'u', ns.LOCAL))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: not u or True)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.OR, (op.NOT, (op.VAR, 'u', ns.LOCAL)), (op.CONST , True)]]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: not (u or True))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.NOT, [op.OR, (op.VAR, 'u', ns.LOCAL), (op.CONST , True)])]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: not u and True)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.AND, (op.NOT, (op.VAR, 'u', ns.LOCAL)), (op.CONST , True)]]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: not (u and True))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.NOT, [op.AND, (op.VAR, 'u', ns.LOCAL), (op.CONST , True)])]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: a or b and c)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.OR, (op.VAR, 'a', ns.GLOBAL), [op.AND, (op.VAR, 'b', ns.GLOBAL), (op.VAR, 'c', ns.GLOBAL)]]]],
				[('u', op.UNDEF)], None, None, ['a', 'b', 'c'], {}
		])

		tree = self.parser.walk(lambda u: a or (b and c))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.OR, (op.VAR, 'a', ns.GLOBAL), [op.AND, (op.VAR, 'b', ns.GLOBAL), (op.VAR, 'c', ns.GLOBAL)]]]],
				[('u', op.UNDEF)], None, None, ['a', 'b', 'c'], {}
		])

		tree = self.parser.walk(lambda u: (a or b) and c)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.AND, [op.OR, (op.VAR, 'a', ns.GLOBAL), (op.VAR, 'b', ns.GLOBAL)], (op.VAR, 'c', ns.GLOBAL)]]],
				[('u', op.UNDEF)], None, None, ['a', 'b', 'c'], {}
		])

		tree = self.parser.walk(lambda u: a and b or c)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.OR, [op.AND, (op.VAR, 'a', ns.GLOBAL), (op.VAR, 'b', ns.GLOBAL)], (op.VAR, 'c', ns.GLOBAL)]]],
				[('u', op.UNDEF)], None, None, ['a', 'b', 'c'], {}
		])

		tree = self.parser.walk(lambda u: a and (b or c))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.AND, (op.VAR, 'a', ns.GLOBAL), [op.OR, (op.VAR, 'b', ns.GLOBAL), (op.VAR, 'c', ns.GLOBAL)]]]],
				[('u', op.UNDEF)], None, None, ['a', 'b', 'c'], {}
		])

		tree = self.parser.walk(lambda u: a and b or c and d)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.OR, 
					[op.AND, (op.VAR, 'a', ns.GLOBAL), (op.VAR, 'b', ns.GLOBAL)], 
					[op.AND, (op.VAR, 'c', ns.GLOBAL), (op.VAR, 'd', ns.GLOBAL)]
				]]],
				[('u', op.UNDEF)], None, None, ['a', 'b', 'c', 'd'], {}
		])

		tree = self.parser.walk(lambda u: a or b and c or d)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.OR, 
					(op.VAR, 'a', ns.GLOBAL), 
					[op.OR, 
						[op.AND, (op.VAR, 'b', ns.GLOBAL), (op.VAR, 'c', ns.GLOBAL)],
						(op.VAR, 'd', ns.GLOBAL)]
				]]],
				[('u', op.UNDEF)], None, None, ['a', 'b', 'c', 'd'], {}
		])


	def test_04list(self):
		tree = self.parser.walk(lambda a,b: (1, plop, a.name, "Zzz", b))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.TUPLE, [
					(op.CONST, 1), (op.VAR, 'plop', ns.GLOBAL), 
					(op.ATTR, (op.VAR, 'a', ns.LOCAL), 'name'),
					(op.CONST, 'Zzz'), (op.VAR, 'b', ns.LOCAL)])]],
				[('a', op.UNDEF), ('b', op.UNDEF)], None, None, ['plop'], {}
		])

		tree = self.parser.walk(lambda a,b: [1, 'plop', True, 3.14, foo])
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.LIST, [
					(op.CONST, 1), (op.CONST, 'plop'), (op.CONST, True), (op.CONST, 3.14), (op.VAR, 'foo', ns.GLOBAL)])]],
				[('a', op.UNDEF), ('b', op.UNDEF)], None, None, ['foo'], {}
		])

		tree = self.parser.walk(lambda u: u[0])
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.AT, (op.VAR, 'u', ns.LOCAL), (op.CONST, 0))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u[:])
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.SLICE, (op.VAR, 'u', ns.LOCAL), None, None)]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u[1:])
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.SLICE, (op.VAR, 'u', ns.LOCAL), (op.CONST, 1), None)]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u[:1])
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.SLICE, (op.VAR, 'u', ns.LOCAL), None, (op.CONST, 1))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u[5:2])
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.SLICE, (op.VAR, 'u', ns.LOCAL), (op.CONST, 5), (op.CONST, 2))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: a in b)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.IN, (op.VAR, 'a', ns.GLOBAL), (op.VAR, 'b', ns.GLOBAL))]],
				[('u', op.UNDEF)], None, None, ['a', 'b'], {}
		])

		tree = self.parser.walk(lambda u: a not in b)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.NIN, (op.VAR, 'a', ns.GLOBAL), (op.VAR, 'b', ns.GLOBAL))]],
				[('u', op.UNDEF)], None, None, ['a', 'b'], {}
		])

	
	def test_05dict(self):
		tree = self.parser.walk(lambda u: {'name': 'doe', 'age': 42})
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.DICT, [
					((op.CONST, 'name'), (op.CONST, 'doe')),
					((op.CONST, 'age') , (op.CONST, 42))
				])]],
				[('u', op.UNDEF)], None, None, [], {}
		])


	def test_06attr(self):
		tree = self.parser.walk(lambda u: u.name)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.ATTR, (op.VAR, 'u', ns.LOCAL), 'name')]],
				[('u', op.UNDEF)], None, None, [], {}
		])


	def test_07funcall(self):
		tree = self.parser.walk(lambda u: u.lower())
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.CALL, (op.ATTR, (op.VAR, 'u', ns.LOCAL), 'lower'), [], {}, None, None]]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: u.lower(a))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.CALL, 
					(op.ATTR, (op.VAR, 'u', ns.LOCAL), 'lower'), [(op.VAR, 'a', ns.GLOBAL)], {}, None, None]]],
				[('u', op.UNDEF)], None, None, ['a'], {}
		])

		tree = self.parser.walk(lambda u, v: u.lower(v, 'b', 3))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.CALL, 
					(op.ATTR, (op.VAR, 'u', ns.LOCAL), 'lower'), 
					[(op.VAR, 'v', ns.LOCAL), (op.CONST, 'b'), (op.CONST, 3)], {}, None, None]]],
				[('u', op.UNDEF), ('v', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u, v: u.lower(v, name='b'))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.CALL, 
					(op.ATTR, (op.VAR, 'u', ns.LOCAL), 'lower'), 
					[(op.VAR, 'v', ns.LOCAL)], {(op.CONST, 'name'): (op.CONST, 'b')}, None, None]]],
				[('u', op.UNDEF), ('v', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u, v: u.lower(*v, **a))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.CALL, 
					(op.ATTR, (op.VAR, 'u', ns.LOCAL), 'lower'), [], {}, (op.VAR, 'v', ns.LOCAL), (op.VAR, 'a', ns.GLOBAL)]]],
				[('u', op.UNDEF), ('v', op.UNDEF)], None, None, ['a'], {}
		])


	def test_08string(self):
		tree = self.parser.walk(lambda u: "::" + u)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.ADD, (op.CONST, '::'), (op.VAR, 'u', ns.LOCAL))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: ":: %s" % u)
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.MOD, (op.CONST, ':: %s'), (op.VAR, 'u', ns.LOCAL))]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		tree = self.parser.walk(lambda u: "%s, %d, %s" % (u.name, u.age, "female"))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, (op.MOD, (op.CONST, '%s, %d, %s'), (op.TUPLE, [ 
					(op.ATTR, (op.VAR, 'u', ns.LOCAL), 'name'),
					(op.ATTR, (op.VAR, 'u', ns.LOCAL), 'age'),
					(op.CONST, 'female')
				]))]],
				[('u', op.UNDEF)], None, None, [], {}
		])
	
	def test_09import(self):
		def func():
			import sys
			import sys as system

			from sys import *
			from sys import stdin, stdout
			from sys import stdin as input, stdout
			from os.path import basename

		tree = self.parser.walk(func)
		self.assertEqual(tree,
			[op.FUNC, 'func', [
				[op.IMPORT, 'sys', []                                    , None    , (op.CONST, -1)],	
				[op.IMPORT, 'sys', []                                    , 'system', (op.CONST, -1)],	
				[op.IMPORT, 'sys', [('*', None)]                         , None    , (op.CONST, -1)],	
				[op.IMPORT, 'sys', [('stdin', None), ('stdout', None)]   , None    , (op.CONST, -1)],	
				[op.IMPORT, 'sys', [('stdin', 'input'), ('stdout', None)], None    , (op.CONST, -1)],	
				[op.IMPORT, 'os.path', [('basename', None)]              , None    , (op.CONST, -1)],	
				[op.RET, (op.CONST, None)]
			], [], None, None, [], {}
		])


	def test_20funcdef(self):
		tree = self.parser.walk(lambda u: foo())
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.CALL, (op.VAR, 'foo', ns.GLOBAL), [], {}, None, None]]],
				[('u', op.UNDEF)], None, None, ['foo'], {}
		])

		# with positional args
		tree = self.parser.walk(lambda u: foo(42, bar))
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.CALL, (op.VAR, 'foo', ns.GLOBAL), [(op.CONST, 42), (op.VAR, 'bar', ns.GLOBAL)], {}, None, None]]],
				[('u', op.UNDEF)], None, None, ['bar', 'foo'], {}
		])


	def test_25ifelse(self):
		# uniline if:else
		tree = self.parser.walk(lambda u: u if True else 'bar')
		self.assertEqual(tree,
			[op.FUNC, op.LAMBDA,
				[[op.RET, [op.IF, (op.CONST, True), [(op.VAR, 'u', ns.LOCAL)], [(op.CONST, 'bar')]]]],
				[('u', op.UNDEF)], None, None, [], {}
		])

		# uniline if:else, result set to a variable
		def func():
			c = a if a else b
			return c
		tree = self.parser.walk(func)
		self.assertEqual(tree,
			[op.FUNC, 'func', [
				(op.SET, (op.VAR, 'c', ns.LOCAL),
					[op.IF, (op.VAR, 'a', ns.GLOBAL), [(op.VAR, 'a', ns.GLOBAL)], [(op.VAR, 'b', ns.GLOBAL)]]
				),
				[op.RET, (op.VAR, 'c', ns.LOCAL)]],
				[], None, None, ['a','b'], {}
		])

		# if:elif:else
		def func():
			if a:
				pass
			elif b:
				pass
			else:
				pass
		tree = self.parser.walk(func)
		self.assertEqual(tree,
			[op.FUNC, 'func', [
					[op.IF, (op.VAR, 'a', ns.GLOBAL), 
						[],
						[[op.IF, (op.VAR, 'b', ns.GLOBAL), [], []]]
					],
					[op.RET, (op.CONST, None)]
				],
				[], None, None, ['a','b'], {}
			])

		# 
		def func():
			a = True

			if a:
				b = 1
			else:
				b = 'plop'
		
			c = 7
		tree = self.parser.walk(func)
		self.assertEqual(tree,
			[op.FUNC, 'func', [
				(op.SET, (op.VAR, 'a', ns.LOCAL), (op.CONST, True)),
				[op.IF, (op.VAR, 'a', ns.LOCAL), 
					[(op.SET, (op.VAR, 'b', ns.LOCAL), (op.CONST, 1))],
					[(op.SET, (op.VAR, 'b', ns.LOCAL), (op.CONST, 'plop'))]
				],
				(op.SET, (op.VAR, 'c', ns.LOCAL), (op.CONST, 7)),
				[op.RET, (op.CONST, None)]
			],
			[], None, None, [], {}
		])

		#
		def func():
			foo()

			if a:
				b = 42
			c
		tree = self.parser.walk(func)
		self.assertEqual(tree,
			[op.FUNC, 'func', [
				[op.CALL, (op.VAR, 'foo', ns.GLOBAL), [], {}, None, None],
				[op.IF, (op.VAR, 'a', ns.GLOBAL), 
					[(op.SET, (op.VAR, 'b', ns.LOCAL), (op.CONST, 42))], 
					[]
				],
				[op.RET, (op.CONST, None)]
			],
			[], None, None, ['a','c','foo'], {}
		])


if __name__ == '__main__':
	unittest.main()
