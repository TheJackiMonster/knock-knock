#!/bin/sh
cd $(dirname $0)
cd ..

APPLICATION_ID="de.thejackimonster.KnockKnock"
PREFIX=/usr/local

if [ $# -gt 1 ]; then
	PREFIX=$1
fi

rm -r $PREFIX/share/icons/hicolor/64x64/apps/$APPLICATION_ID.png
rm -r $PREFIX/share/icons/hicolor/128x128/apps/$APPLICATION_ID.png
rm -r $PREFIX/share/icons/hicolor/256x256/apps/$APPLICATION_ID.png
rm -r $PREFIX/share/icons/hicolor/512x512/apps/$APPLICATION_ID.png
rm -r $PREFIX/share/icons/hicolor/scalable/apps/$APPLICATION_ID.svg

rm -f $PREFIX/share/applications/$APPLICATION_ID.desktop
rm -rf $PREFIX/share/knock-knock/
rm -f $PREFIX/bin/knock-knock
