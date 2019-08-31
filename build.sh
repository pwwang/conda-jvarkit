#!/usr/bin/env bash

DIST="$PREFIX/opt/jvarkit"
if [[ ! -e $DIST ]]; then
	mkdir -p $DIST
fi
cp -r * $DIST
cd $DIST

cp $RECIPE_DIR/jvarkit.template.py $PREFIX/bin/jvarkit

sed -i "s#{{version}}#${PKG_VERSION}#g" $PREFIX/bin/jvarkit
sed -i "s#{{rev}}#$PKG_BUILD_STRING#g" $PREFIX/bin/jvarkit
sed -i "s#{{jardir}}#$DIST/dist#g" $PREFIX/bin/jvarkit

chmod +x $PREFIX/bin/jvarkit
