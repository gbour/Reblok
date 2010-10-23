#!/usr/bin/env python

__version__ = "$Revision$ $Date$"

from distutils.core import setup

setup(
	name         = 'reblok',
	version      = '0.1.0',
	description  = 'Python decompiler',
	author       = 'Guillaume Bour',
	author_email = 'guillaume@bour.cc',
	url          = 'http://devedge.bour.cc/wiki/Reblok/',
	license      = 'GPL v3',

	packages=['reblok'],
	requires=['byteplay'],
)
