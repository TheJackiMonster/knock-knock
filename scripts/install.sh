#!/bin/sh
cd $(dirname $0)
cd ..

mkdir -p /usr/local/share/knock-knock
cp AUTHORS /usr/local/share/knock-knock/AUTHORS
cp LICENSE /usr/local/share/knock-knock/LICENSE
cp door.py /usr/local/share/knock-knock/door.py
cp door.sh /usr/local/share/knock-knock/door.sh
cp door.ui /usr/local/share/knock-knock/door.ui
cp door_row.ui /usr/local/share/knock-knock/door_row.ui
cp new_door_dialog.ui /usr/local/share/knock-knock/new_door_dialog.ui
cp edit_door_dialog.ui /usr/local/share/knock-knock/edit_door_dialog.ui

mkdir -p /usr/local/bin
cp bin/door /usr/local/bin/knock-knock

mkdir -p /usr/local/share/applications
cp door.desktop /usr/local/share/applications/knock-knock.desktop
