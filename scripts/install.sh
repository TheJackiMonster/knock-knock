#!/bin/sh
cd $(dirname $0)
cd ..

APPLICATION_ID="de.thejackimonster.KnockKnock"

mkdir -p /usr/local/share/knock-knock
cp AUTHORS /usr/local/share/knock-knock/AUTHORS
cp LICENSE /usr/local/share/knock-knock/LICENSE
cp door.py /usr/local/share/knock-knock/door.py
cp door.sh /usr/local/share/knock-knock/door.sh
cp -r ui /usr/local/share/knock-knock/ui

mkdir -p /usr/local/icons/hicolor/64x64/apps
mkdir -p /usr/local/icons/hicolor/128x128/apps
mkdir -p /usr/local/icons/hicolor/256x256/apps
mkdir -p /usr/local/icons/hicolor/512x512/apps
mkdir -p /usr/local/icons/hicolor/scalable/apps

cp icon/64x64.png /usr/local/share/icons/hicolor/64x64/apps/$APPLICATION_ID.png
cp icon/128x128.png /usr/local/share/icons/hicolor/128x128/apps/$APPLICATION_ID.png
cp icon/256x256.png /usr/local/share/icons/hicolor/256x256/apps/$APPLICATION_ID.png
cp icon/512x512.png /usr/local/share/icons/hicolor/512x512/apps/$APPLICATION_ID.png
cp knock-knock.svg /usr/local/share/icons/hicolor/scalable/apps/$APPLICATION_ID.svg

mkdir -p /usr/local/bin
cp bin/knock-knock /usr/local/bin/knock-knock

mkdir -p /usr/local/share/applications
cp knock-knock.desktop /usr/local/share/applications/$APPLICATION_ID.desktop

gtk-update-icon-cache -t /usr/local/share/icons/hicolor
update-desktop-database
