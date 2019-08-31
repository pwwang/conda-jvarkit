#!/usr/bin/env python
__version__ = '{{version}}-{{rev}}'

from pathlib import Path
JARDIR = Path('{{jardir}}')

try:
	import cmdy
	from pyparam import commands
except ImportError:
	# conda can't specify pip dependencies
	import pip
	def pip_install(package):
		if hasattr(pip, 'main'):
			pip.main(['install', package])
		else:
			pip._internal.main(['install', package])
	pip_install('cmdy')
	pip_install('pyparam')

commands._.version = False
commands._.version = 'Show current version of jvarkit.'
commands.install = 'Install a jvarkit tool.'
commands.install._.required = True
commands.install._.desc = 'The jvarkit tool to be installed. Use "jvarkit list" to see all available tools.'
commands.list = 'List available jvarkit tools.'
commands.list._hbald = False
commands.version = 'Show current version of jvarkit.'

def is_installed(tool):
	return (JARDIR / (tool + '.jar')).exists()

def list_tools():
	print("")
	print("INSTALLED | TOOL")
	print("--------- | --------------------")
	for d in (JARDIR.parent / 'src/main/java/com/github/lindenb/jvarkit/tools').iterdir():
		if d.is_dir():
			print("%s         | %s" % (is_installed(d.name), d.name))

def show_version():
	print('jvarkit v%s built by conda-jvarkit.' % __version__)

if __name__ == '__main__':
	command, opts, gopts = commands._parse(arbi = True)
	if command == 'version' or gopts['version']:
		show_version()
	if command == 'list':
		list_tools()
	if command == 'vcfstats':
		pass

