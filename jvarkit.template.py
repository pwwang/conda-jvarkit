#!/usr/bin/env python
__version__ = '{{version}}-{{rev}}'

from os import environ
from pathlib import Path
from xml.etree import ElementTree
from functools import lru_cache

def try_import(package):
	try:
		return __import__(package)
	except ImportError:
		from sys import executable
		from subprocess import check_call
		check_call([executable, '-m', 'pip', 'install', package])
	finally:
		return __import__(package)

cmdy     = try_import('cmd')
commands = getattr(try_import('pyparam'), 'commands')

JARDIR = Path('{{jardir}}')

commands._.version          = False
commands._.version.desc     = 'Show current version of jvarkit.'
commands._.jardir           = ''
commands._.jardir.show      = False
commands._.jardir.desc      = 'The directory containing jar files for jvarkit tools, only used in development mode.'
commands.install            = 'Install a jvarkit tool.'
commands.install._.required = True
commands.install._.desc     = 'The jvarkit tool to be installed. Use "jvarkit list" to see all available tools.'
commands.list               = 'List available jvarkit tools.'
commands.list._hbald        = False
commands.version            = 'Show current version of jvarkit.'

def is_installed(tool):
	return (JARDIR / (tool + '.jar')).exists()

@lru_cache()
def get_tools():
	ret  = {}
	root = ElementTree.parse(JARDIR.parent / 'docs' / 'index.html')
	trs  = root.find('body/div/table/tbody')
	for tr in trs.iterfind('tr'):
		tool = tr.find('th/a').text
		if tool:
			ret[tool] = tr.find('td').text
	return ret

def list_tools():
	print("")
	print("INSTALLED | TOOL                       | DESCRIPTION")
	print("--------- | -------------------------- | -----------------------------------------------------------")

	tools = get_tools()
	for tool, desc in tools.items():
		print("%-9s | %-26s | %s" % ('YES' if is_installed(tool) else 'NO', tool, desc))

def show_version():
	print('jvarkit v%s built by conda-jvarkit.' % __version__)

if __name__ == '__main__':
	command, opts, gopts = commands._parse(arbi = True)
	#print(command, opts, gopts)
	if gopts['jardir']:
		JARDIR = Path(gopts['jardir'])
	if command == 'version' or gopts['version']:
		show_version()
	if command == 'list':
		list_tools()
	if command == 'vcfstats':
		pass

