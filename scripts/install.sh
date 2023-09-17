#!/bin/sh
cd $(dirname $0)
cd ..

mkdir -p /usr/local/share/haxko-door
cp door.py /usr/local/share/haxko-door/door.py
cp door.sh /usr/local/share/haxko-door/door.sh
cp door.ui /usr/local/share/haxko-door/door.ui

mkdir -p /usr/local/bin
cp bin/door /usr/local/bin/door

mkdir -p /usr/local/share/applications
cp door.desktop /usr/local/share/applications/door.desktop
