# Knock Knock

Application to interact with SSH doors

![Icon of the application](resources/de.thejackimonster.KnockKnock.svg)

## Features

This application is used to interact with door locks via SSH over local network (typically Wi-Fi). It's intended to mirror some functionality of the Android app called "Trigger" which is available via [F-Droid](https://f-droid.org/de/packages/com.example.trigger/). However this application is using GTK+ with some widgets from libhandy to provide a usable interface for mobile Linux devices.

## Installation

The repository provides simple bash scripts to install (and uninstall) the application easily using following commands:

 - `./scripts/install.sh` to install the application (this might require sudo privileges)
 - `./scripts/uninstall.sh` to uninstall the application (this might require sudo privileges)

Once installed the application can also be used via its desktop application likely appearing as interactable icon in your desktop shell. Alternatively you can launch it via the short command: `knock-knock`

Should you prefer to not install the application but running it more lightly in a portable way, you can simply navigate into the directory of the cloned/downloaded repository and run the main Python script via: `./door.py`

## Usage

The application starts the first time without any configurations for existing doors. So a first step will be adding such a configuration for a door (or another device) you like to interact with via SSH.

Simply swipe the menu on the left side of the window into the screen or open it via its dedicated button in the left upper corner. Then click on the '+' button to create a new configuration and enter necessary details.

You can still change most details in a later stage via the settings button in the right upper corner and every configurations gets listed via its unique name. So you can select which one to use or scan for in your local network.

Notice that this application uses the `ssh` and the `ping` command internally. So that's required to be installed as well as 'gtk3', 'libhandy', 'libgio' and 'glib'.

