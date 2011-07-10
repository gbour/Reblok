#!/usr/bin/env python
# -*- coding: UTF8 -*-

import sys, marshal
import byteplay as byte
from reblok import *

import pprint

DEPTH=0

def iprint(msg, newline=True):
	global DEPTH

	print "%s%s" % ('\t'*DEPTH, msg),
	if newline:
		print

def dispatch(instr, **kwargs):
	return eval('do_%s' % instr[0].replace(' ', '_'))(instr, **kwargs)

### CONST,VAR ###
def do_const(instr, **kwargs):
	if instr[1] is None:
		return 'None'
	elif isinstance(instr[1], str):
		return "'%s'" % instr[1].replace('\n', '\\n')

	return str(instr[1])

def do_var(instr, **kwargs):
	return instr[1]

def do_attr(instr, **kwargs):
	return "%s.%s" % (dispatch(instr[1], **kwargs), instr[2])

def do_at(instr, **kwargs):
	return "%s[%s]" % (dispatch(instr[1]), dispatch(instr[2]))

def do_not_in(instr, **kwargs):
	return "%s not in %s" % (dispatch(instr[1]), dispatch(instr[2]))

def do_neq(instr, **kwargs):
	return "%s != %s" % (dispatch(instr[1]), dispatch(instr[2]))

def do_and(instr, **kwargs):
	return "%s and %s" % (dispatch(instr[1]), dispatch(instr[2]))

def do_add(instr, **kwargs):
	return "%s + %s" % (dispatch(instr[1]), dispatch(instr[2]))

def do_sub(instr, **kwargs):
	return "%s - %s" % (dispatch(instr[1]), dispatch(instr[2]))

def do_in(instr, **kwargs):
	return "%s in %s" % (dispatch(instr[1]), dispatch(instr[2]))

def do_slice(instr, **kwargs):
	return "[%s:%s]" % ('' if instr[1] is None else dispatch(instr[1]), '' if instr[2] is None else dispatch(instr[2]))

def do_lt(instr, **kwargs):
	return "%s < %s" % (dispatch(instr[1]), dispatch(instr[2]))

def do_positive(instr, **kwargs):
	return "+%s" % (dispatch(instr[1]))

def do_negative(instr, **kwargs):
	return "-%s" % (dispatch(instr[1]))

### OPERATORS ###
def do_eq(instr, **kwargs):
	right = dispatch(instr[2], noprint=True)
	return "%s %s %s" % (dispatch(instr[1], noprint=True), 'is' if right == 'None' else '==', right)

def do_mod(instr, **kwargs):
	return "%s %% %s" % (dispatch(instr[1], noprint=True), dispatch(instr[2], noprint=True))

def do_mul(instr, **kwargs):
	return "%s * %s" % (dispatch(instr[1], noprint=True), dispatch(instr[2], noprint=True))

def do_list(instr, **kwargs):
	ret = "[%s]" % (', '.join([dispatch(i, noprint=True) for i in instr[1]]))
	if 'noprint' not in kwargs:
		iprint(ret)

	return ret

def do_import(instr, **kwargs):
	if instr[2] is None:
		iprint("import %s" % instr[1], False)

		if instr[3] is not None:
			iprint("as %s" % instr[3], False)
		iprint('', True)
	else:
		iprint("from %s import %s" % (instr[1], instr[2]))

def do_function(instr, **kwargs):
	global DEPTH

	if instr[1] == 'lambda':
		ret = 'lambda %s: %s' % (', '.join([arg[0] for arg in instr[3]]), dispatch(instr[2][0][1], noprint=True))

		if 'noprint' not in kwargs:
			print ret
		return ret

	iprint("")
	iprint("def %s():" % instr[1])
	DEPTH += 1

	for instr in instr[2]:
		dispatch(instr)
	DEPTH -= 1

def do_if(instr, **kwargs):
	if 'noprint' in kwargs:
		return "%s if %s else %s" % (dispatch(instr[2][0], noprint=True), dispatch(instr[1], noprint=True), dispatch(instr[3][0], noprint=True))

	global DEPTH
	iprint('');
	iprint("if %s:" % (dispatch(instr[1])))
	DEPTH += 1

	for instr in instr[2]:
		dispatch(instr)

	DEPTH -= 1

def do_ret(instr, **kwargs):
	iprint("return %s" % dispatch(instr[1], noprint=True))

def do_call(instr, **kwargs):
	_args=""
	if instr[4] is not None:
		_args = ", **%s" % dispatch(instr[4], noprint=True)

	_kwargs=""
	if instr[5] is not None:
		_kwargs = ", **%s" % dispatch(instr[5], noprint=True)

	named = ', '.join(["%s=%s" % (dispatch(k, noprint=True)[1:-1], dispatch(instr[3][k], noprint=True)) for k in instr[3].keys()])
	if len(named) > 0:
		named = ', %s' % named

	ret = "%s(%s%s%s%s)" % (\
			dispatch(instr[1], noprint=True), 
			', '.join([dispatch(x, noprint=True) for x in instr[2]]), 
			named,_args, _kwargs)

	if 'noprint' not in kwargs:
		iprint(ret)

	return ret

def do_print(instr, **kwargs):
	stream = dispatch(instr[1], noprint=True)
	if stream == "sys.stdout":
		stream = ""
	else:
		stream = " >>", stream

	if instr[2][-1] == ('const', '\n'):
		instr[2].pop()
	iprint("print%s %s" % (stream, ', '.join([dispatch(x, noprint=True) for x in instr[2]])))

def do_set(instr, **kwargs):
	iprint("%s = %s" % (dispatch(instr[1]), dispatch(instr[2], noprint=True)))

def do_for(instr, **kwargs):
	global DEPTH
	# list comprehension
	if len(instr[3]) == 1 and instr[3][0][0] == 'append':
		ret = "[%s for %s in %s]" % (dispatch(instr[3][0][2]), instr[1], dispatch(instr[2], noprint=True))

		if 'noprint' not in kwargs:
			iprint(ret)
		return ret

	iprint("for %s in %s:" % (instr[1], dispatch(instr[2], noprint=True)))
	DEPTH += 1
	
	for instr in instr[3]:
		dispatch(instr)
	DEPTH -= 1

if __name__ == '__main__':
	#c = byte.Code.from_code(code.func_code)
	#print c.code
	print sys.argv
	f = open(sys.argv[0])
	c = f.read()
	f.close()

	import compiler
	compiler.compileFile(sys.argv[0])


	f = open(sys.argv[1])
	f.seek(8)

	o = marshal.load(f)
	f.close()

	print o, dir(o)
	import dis
#	dis.dis(o)
#	print o.co_consts
#	dis.dis(o.co_consts[2])

	# function definition is LOAD_CONST argument
	c = byte.Code.from_code(o)
	print c.code
	print "plop function:",\
	      filter(lambda x: isinstance(x[1], byte.Code), c.code)[0][1].code

	res = Parser().walk(o)
	print "\n=== tree"
	import pprint; pprint.pprint(res)
	print "\n=== python"
	for instr in res:
		dispatch(instr)
