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

cmdy        = try_import('cmdy')
commands    = getattr(try_import('pyparam'), 'commands')

JARDIR = Path('{{jardir}}')
# for development
if '{{' in str(JARDIR) and '}}' in str(JARDIR):
	JARDIR = Path(environ.get('JVARKIT_JARDIR', ''))

@lru_cache()
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

@lru_cache()
def tool_help(tool, java = 'java'):
	return str(cmdy.java('-jar', str(JARDIR / (tool + '.jar')), h = True, _exe = java))

def helpx(helps):
	helps.delete('Global optional options')
	helps.delete('Available commands')
	helps.add('Available commands')
	helps.select('Available commands').addCommand(commands.install, ['install']) \
		.addCommand(commands.list, ['list']) \
		.addCommand(commands.version, ['version']) \
		.addCommand(commands.help, ['help'], ishelp = True)
	sec = helps.add('Installed tools', sectype = 'option')['Installed tools']
	for tool, desc in get_tools().items():
		if is_installed(tool):
			sec.add((tool, '', desc))

def tool_helpx(tool):
	def help_callback(helps):
		helps.add('Java options', [
			('-X../-D..', '', 'Java Virtual Machine Parameters')
		])
		req_sec = helps.add('Required tool options', sectype = 'options')['Required tool options']
		opt_sec = helps.add('Optional tool options', sectype = 'options')['Optional tool options']
		tool_help_lines = tool_help(tool).splitlines()
		started = False
		option = {'raw': None, 'req': False}
		def addoption(option):
			if not option['raw']:
				return
			(req_sec if option['req'] else opt_sec).add(tuple(option['raw']))
			option['raw'], option['req'] = None, False

		for line in tool_help_lines:
			line = line.strip()
			if line.startswith('Options'):
				started = True
				continue
			if not started:
				continue
			if line.startswith('-'):
				addoption(option)
				option['raw'] = [line, '', []]
			elif line.startswith('* -'):
				addoption(option)
				option['req'] = True
				option['raw'] = [line[2:], '', []]
			else:
				option['raw'][2].append(line)
		addoption(option)

	return help_callback

commands.install            = 'Install a jvarkit tool.'
commands.install._.required = True
commands.install._.desc     = ['The jvarkit tool to be installed.',
							   'Use "jvarkit list" to see all available tools.',
							   'Use "jvarkit install all" to install all tools.']
commands.list               = 'List available jvarkit tools.'
commands.list._hbald        = False
commands.version            = 'Show current version of jvarkit.'

for tool, desc in get_tools().items():
	if is_installed(tool):
		commands[tool] = str(desc)
		commands[tool]._helpx = tool_helpx(tool)
		commands[tool].hh = False
		commands[tool].hh.desc = 'Show original help page.'
		commands[tool].java = 'java'
		commands[tool].java.desc = 'Path to java executable.'

commands._helpx = helpx

def list_tools():
	print("")
	print("INSTALLED | TOOL                       | DESCRIPTION")
	print("--------- | -------------------------- | -----------------------------------------------------------")

	tools = get_tools()
	for tool, desc in tools.items():
		print("%-9s | %-26s | %s" % ('YES' if is_installed(tool) else 'NO', tool, desc))

def show_version():
	print('jvarkit v%s built by conda-jvarkit.' % __version__)

def install_tool(tool):
	cmdy.gradlew(_fg = True, _exe = str(JARDIR.parent / 'gradlew'), p = str(JARDIR.parent), _ = tool)


def run_tool(tool, opts):
	for hopt in commands[tool]._hopts:
		del opts[hopt]

	java     = opts.pop('java')
	hh       = opts.pop('hh')
	javaopts = [pos for pos in opts.get('_', []) if pos[:2] in ('-X', '-D')]

	opts['_'] = [pos for pos in opts.get('_', []) if pos[:2] not in ('-X', '-D')]
	javaopts.append('-jar')
	javaopts.append(str(JARDIR / (tool + '.jar')))
	if hh:
		print(tool_help(tool, java))
		return
	opts['_fg']  = True
	opts['_exe'] = java
	try:
		cmdy.java(*javaopts, **opts)
	except cmdy.CmdyReturnCodeException:
		commands[tool]._help(print_and_exit = True)

if __name__ == '__main__':

	command, opts, _ = commands._parse(arbi = True)

	if command == 'help':
		commands._help(print_and_exit = True)
	elif command == 'install':
		install_tool(opts['_'])
	elif command == 'version':
		show_version()
	elif command == 'list':
		list_tools()
	elif command not in get_tools():
		commands._help(error = 'No such command/tool: %s' % command, print_and_exit = True)
	elif not is_installed(command):
		print('Tool "%s" is not installed, try "jvarkit install %s" to install it' % (command, command))
	else:
		run_tool(command, opts)
