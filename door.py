#!/bin/python3
# -*- coding: utf-8 -*-

import gi
import subprocess

gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")

from gi.repository import GObject, GLib, Gtk, Handy

Handy.init()

door_address = "192.168.178.2"
idle_task = None

def main():
    builder = Gtk.Builder()
    builder.add_from_file("door.ui")

    window = builder.get_object("window")
    window.connect("destroy", Gtk.main_quit)
    
    header_bar = builder.get_object("header_bar")

    refresh_button = builder.get_object("refresh_button")
    open_button = builder.get_object("open_button")
    close_button = builder.get_object("close_button")
    cancel_button = builder.get_object("cancel_button")

    state_stack = builder.get_object("state_stack")
    error_label = builder.get_object("error_label")

    def task_searching():
        global door_address
        global idle_task

        try:
            code = subprocess.call("ping -c 1 %s" % door_address, shell=True)
        except:
            code = 1

        if code == 0:
            set_state("ready")
        else:
            set_state("error")

        idle_task = None
        return False

    def task_open():
        global door_address
        global idle_task

        try:
            result = subprocess.Popen("ssh auf@%s" % door_address, shell=True, stdout=subprocess.PIPE).stdout.read()
        except:
            result = "ERROR"

        if result == "UNLOCKED":
            set_state("ready")
        else:
            set_state("error")

        idle_task = None
        return False
    
    def task_close():
        global door_address
        global idle_task

        try:
            result = subprocess.Popen("ssh zu@%s" % door_address, shell=True, stdout=subprocess.PIPE).stdout.read()
        except:
            result = "ERROR"

        if result == "LOCKED":
            set_state("ready")
        else:
            set_state("error")

        idle_task = None
        return False

    def set_state(state, msg=None):
        global idle_task

        if state == "ready":
            refresh_button.set_sensitive(True)
            open_button.set_sensitive(True)
            close_button.set_sensitive(True)
            cancel_button.set_sensitive(False)
        elif state == "error":
            refresh_button.set_sensitive(True)
            open_button.set_sensitive(False)
            close_button.set_sensitive(False)
            cancel_button.set_sensitive(False)

            if msg is not None:
                error_label.set_text(msg)
        else:
            refresh_button.set_sensitive(False)
            open_button.set_sensitive(False)
            close_button.set_sensitive(False)
            cancel_button.set_sensitive(True)

        if idle_task is not None:
            GLib.source_remove(idle_task)

        if state == "searching":
            idle_task = GLib.idle_add(task_searching)
        elif state == "opening":
            idle_task = GLib.idle_add(task_open)
        elif state == "closing":
            idle_task = GLib.idle_add(task_close)
        else:
            idle_task = None

        state_stack.set_visible_child_name(state)

    def refresh(_button):
        set_state("searching")

    def open_door(_button):
        set_state("opening")

    def close_door(_button):
        set_state("closing")

    def cancel(_button):
        set_state("ready")

    refresh_button.connect("clicked", refresh)
    open_button.connect("clicked", open_door)
    close_button.connect("clicked", close_door)
    cancel_button.connect("clicked", cancel)

    set_state("searching")

    window.show()
    Gtk.main()

if __name__ == "__main__":
    main()
