#!/usr/bin/env python

__version__ = "$Revision$ $Date$"

import subprocess
from distutils.core import setup, Command

class BuildDebianPackage(Command):
	description = "create a debian package"
	user_options = []

	def initialize_options(self):
		pass

	def finalize_options(self):
		pass

	def run(self):
		subprocess.call(['dpkg-buildpackage'])

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

	cmdclass={'bdist_deb': BuildDebianPackage}
)
