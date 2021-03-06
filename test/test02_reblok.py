#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
    reblok, python decompiler, AST builder
    Copyright (C) 2010-2011, Guillaume Bour <guillaume@bour.cc>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
__author__  = "Guillaume Bour <guillaume@bour.cc>"
__version__ = "$Revision$"
__date__    = "$Date$"
__license__ = "GPLv3"

import unittest, sys, os, os.path, compileall, subprocess, tempfile, marshal
import byteplay
from reblok import Parser, namespaces as ns, opcodes as op

class TestReblokBasics(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		unittest.TestCase.__init__(self, *args, **kwargs)
		self.parser = Parser()

		# compile snippets
		self.snippets = os.path.join(os.path.dirname(sys.argv[0]), 'snippets')
		compileall.compile_dir(self.snippets)

	def walk(code):
		return self.parser.walk(code)

	def test_01reblok(self):
		for root, dirs, files in os.walk(self.snippets):
			for f in files:
				if not f.endswith('.pyc'):
					continue

				tmp = tempfile.mkstemp(prefix='reblok-')
				print os.path.join(root,f), tmp, type(tmp)
				ret = subprocess.call(['reblok', os.path.join(root, f)], stdout=tmp[0])
				# validation #1: reblok mist return 0 value
				self.assertEqual(ret, 0)

				# validation #2: we compare AST generated by source file and reblok-output
				# file
				with open(os.path.join(root,f)) as fh:
					fh.seek(8)
					bytecode = marshal.load(fh)

				tree = Parser().walk(bytecode)

				try:
					with open(tmp[1]) as fh:
						bytecode = compile(fh.read(), '<string>', 'exec')
				except SyntaxError:
					self.fail('%s: invalid source file (%s)' % (f, tmp[1]))

				tree2 = Parser().walk(bytecode)
				import pprint; pprint.pprint(tree); pprint.pprint(tree2)
				self.assertEqual(tree, tree2)



if __name__ == '__main__':
	unittest.main()

