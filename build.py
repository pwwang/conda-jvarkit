#!/usr/bin/env python

from pathlib import Path
from functools import lru_cache
import yaml
import requests
import cmdy
from pyparam import commands
from liquid import Liquid
HERE     = Path(__file__).parent.resolve()
METAFILE = HERE / 'meta.yaml'
METATPL  = HERE / 'meta.template.yaml'
JVARKIT  = HERE / 'jvarkit.py'
JVKITPL  = HERE / 'jvarkit.template.py'

commands.check             = 'Check if jvarkit is up-to-date.'
commands.check._hbald      = False
commands.build             = 'Check and build conda package for jvarkit if it is outdated.'
commands.build._hbald      = False
commands.build.force       = False
commands.build.force.desc  = 'Build the package anyway, even if it is up-to-date.'
commands.build.rev.desc    = 'Build the package at this revision, implies "--force".'
commands.build.upload      = False
commands.build.upload.desc = 'Upload the package after build.'

@lru_cache()
def get_latest_jvarkit_version():
	api = "https://api.github.com/repos/lindenb/jvarkit/commits"
	commit = requests.get(api).json()[0]
	return commit["commit"]["committer"]["date"].split("T")[0], commit["sha"]

@lru_cache()
def get_current_jvarkit_version():
	if not METAFILE.exists():
		return "", ""
	with METAFILE.open() as f:
		meta = yaml.safe_load(f)
	try:
		return meta['package']['version'].replace('.', '-'), meta['build']['string']
	except:
		return "", ""

@lru_cache()
def get_date_of_commit(commit):
	api = "https://api.github.com/repos/lindenb/jvarkit/commits/" + commit
	print( requests.get(api).json())
	return requests.get(api).json()["commit"]["committer"]["date"].split("T")[0]

def build_jvarkit(rev, date = None):
	date = date or get_date_of_commit(rev)
	print("- Rendering meta.yaml ...")
	METAFILE.write_text(Liquid(METATPL.read_text()).render(
		version = date.replace('-', '.'),
		rev = rev[:7]
	))

	print("- Start bulding the package ...")
	cmdy.conda.build(HERE).fg

def check():
	print("- Checking if jvarkit build is up-to-date ...")
	curr_date, curr_version = get_current_jvarkit_version()
	print(f"  Current build is on {curr_date}, at revision {curr_version}.")
	latest_date, latest_version = get_latest_jvarkit_version()
	print(f"  Latest commit is on {latest_date}, at revision {latest_version}.")
	if not curr_date:
		print("  The build is outdated.")
		return True
	curr_date = [int(d) for d in curr_date.split('-')]
	late_date = [int(d) for d in latest_date.split('-')]
	if late_date > curr_date:
		print(" The build is outdated.")
		return True
	print(" The build is up-to-date.")
	return False

def build(opts):
	should_upload = False
	if opts['rev']:
		build_jvarkit(opts['rev'])
		should_upload = True
	elif opts['force']:
		latest_date, latest_version = get_latest_jvarkit_version()
		build_jvarkit(latest_version, latest_date)
		should_upload = True
	else:
		checked = check()
		if not checked:
			print("- Skip building.")
			should_upload = False
		else:
			latest_date, latest_version = get_latest_jvarkit_version()
			build_jvarkit(latest_version, latest_date)
			should_upload = True
	if should_upload and opts['upload']:
		upload()

def upload(opts):
	pass

if __name__ == "__main__":
	command, opts, _ = commands._parse()
	if command == "check":
		check()
	elif command == "build":
		build(opts)
