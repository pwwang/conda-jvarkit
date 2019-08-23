#!/usr/bin/env bash

DIST="$PREFIX/opt/jvarkit"
if [[ ! -e $DIST ]]; then
	mkdir -p $DIST
fi
cp -r * $DIST
cd $DIST
