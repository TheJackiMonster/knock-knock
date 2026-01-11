#!/bin/sh
cd $(dirname $0)
cd ..

APPLICATION_ID="de.thejackimonster.KnockKnock"
PREFIX=/usr/local

SKIP_UPDATE=0

while [ $# -gt 0 ]; do
	if [ $1 == "--skip-update" ]; then
		SKIP_UPDATE=1
	else
		PREFIX=$1
	fi

	shift
done

mkdir -p $PREFIX/share/knock-knock
cp AUTHORS $PREFIX/share/knock-knock/AUTHORS
cp LICENSE $PREFIX/share/knock-knock/LICENSE
cp door.py $PREFIX/share/knock-knock/door.py
cp knock.py $PREFIX/share/knock-knock/knock.py
cp door.sh $PREFIX/share/knock-knock/door.sh
cp -r resources/ $PREFIX/share/knock-knock/

mkdir -p $PREFIX/share/icons/hicolor/64x64/apps
mkdir -p $PREFIX/share/icons/hicolor/128x128/apps
mkdir -p $PREFIX/share/icons/hicolor/256x256/apps
mkdir -p $PREFIX/share/icons/hicolor/512x512/apps
mkdir -p $PREFIX/share/icons/hicolor/scalable/apps

cp resources/icon/64x64.png $PREFIX/share/icons/hicolor/64x64/apps/$APPLICATION_ID.png
cp resources/icon/128x128.png $PREFIX/share/icons/hicolor/128x128/apps/$APPLICATION_ID.png
cp resources/icon/256x256.png $PREFIX/share/icons/hicolor/256x256/apps/$APPLICATION_ID.png
cp resources/icon/512x512.png $PREFIX/share/icons/hicolor/512x512/apps/$APPLICATION_ID.png
cp resources/$APPLICATION_ID.svg $PREFIX/share/icons/hicolor/scalable/apps/$APPLICATION_ID.svg

mkdir -p $PREFIX/bin
echo "#!/bin/sh" > $PREFIX/bin/knock-knock
echo "sh $PREFIX/share/knock-knock/door.sh" >> $PREFIX/bin/knock-knock
chmod +x $PREFIX/bin/knock-knock

mkdir -p $PREFIX/share/applications
cp resources/$APPLICATION_ID.desktop $PREFIX/share/applications/$APPLICATION_ID.desktop

if [ $SKIP_UPDATE -gt 0 ]; then
	exit
fi

gtk-update-icon-cache -f -t $PREFIX/share/icons/hicolor
update-desktop-database
