#!/bin/sh
cd $(dirname $0)
cd ..

APPLICATION_ID="de.thejackimonster.KnockKnock"

rm -r /usr/local/share/icons/hicolor/64x64/apps/$APPLICATION_ID.png
rm -r /usr/local/share/icons/hicolor/128x128/apps/$APPLICATION_ID.png
rm -r /usr/local/share/icons/hicolor/256x256/apps/$APPLICATION_ID.png
rm -r /usr/local/share/icons/hicolor/512x512/apps/$APPLICATION_ID.png
rm -r /usr/local/share/icons/hicolor/scalable/apps/$APPLICATION_ID.svg

rm -f /usr/local/share/applications/$APPLICATION_ID.desktop
rm -rf /usr/local/share/knock-knock/
rm -f /usr/local/bin/knock-knock
