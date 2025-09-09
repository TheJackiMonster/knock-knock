#!/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Tobias Frisch"
__copyright__ = "Copyright 2025, Tobias Frisch"
__credits__ = "Tobias Frisch"

__license__ = "GPL"
__license_version__ = "3.0.0"

__maintainer__ = "Tobias Frisch"
__email__ = "jacki@thejackimonster.de"
__status__ = "Production"
__version__ = "0.0.1"

import base64
import gi
import json
import os
import subprocess

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
gi.require_version("Handy", "1")

from gi.repository import Gio, GLib, GObject, Gdk, Gtk, Handy

Handy.init()


application_id = "de.thejackimonster.KnockKnock"
file_encoding = "utf-8"
string_encoding = "utf-8"

app = Gtk.Application.new(application_id, Gio.ApplicationFlags.FLAGS_NONE)

css = ".flap-background { background-color: @theme_bg_color; }"


class Door:

    name = ""

    address = "127.0.0.1"
    port = 22

    open_cmd = "open"
    close_cmd = "close"
    state_cmd = "state"

    locked_val = "LOCKED"
    unlocked_val = "UNLOCKED"

    filename = None
    widget = None


    def equals(self, other):
        if self.name != other.name:
            return False
        
        if self.address != other.address:
            return False
        if self.port != other.port:
            return False
        
        if self.open_cmd != other.open_cmd:
            return False
        if self.close_cmd != other.close_cmd:
            return False
        if self.state_cmd != other.state_cmd:
            return False
        
        if self.locked_val != other.locked_val:
            return False
        if self.unlocked_val != other.unlocked_val:
            return False
        
        return True
    


class DoorCollection:

    select_door = None
    list_doors = None
    add_door = None
    remove_door = None
    reload_door = None


collection = DoorCollection()
current = None


def load_door(path):
    if (not os.path.isfile(path)) or (not os.path.exists(path)):
        return None
    
    door = Door()

    with open(path, "r", encoding=file_encoding) as f:
        data = json.loads(f.read())

        if not data:
            return None
        
        door.name = str(data['name'])
        door.address = str(data['host'])
        door.port = int(data['port'])
        door.open_cmd = str(data['open_command'])
        door.close_cmd = str(data['close_command'])
        door.state_cmd = str(data['state_command'])
        door.locked_val = str(data['locked_pattern'])
        door.unlocked_val = str(data['unlocked_pattern'])

    door.filename = os.path.basename(path)
    return door


def store_door(path, door):
    with open(path, "w", encoding=file_encoding) as f:
        f.write(json.dumps({
            'name': str(door.name),
            'host': str(door.address),
            'port': int(door.port),
            'open_command': str(door.open_cmd),
            'close_command': str(door.close_cmd),
            'state_command': str(door.state_cmd),
            'locked_pattern': str(door.locked_val),
            'unlocked_pattern': str(door.unlocked_val),
        }))


def delete_door(path):
    if (not os.path.isfile(path)) or (not os.path.exists(path)):
        return None
    
    os.remove(path)


def get_doors_data_dir():
    data_home = os.environ.get('XDG_DATA_HOME') or \
        os.path.join(os.path.expanduser('~'), '.local', 'share')
    data_dir = os.path.join(data_home, application_id)

    return data_dir


def door_get_path(door):
    data_dir = get_doors_data_dir()
    filename = None
    
    if door.filename:
        filename = door.filename
    elif door.name:
        filename = str(base64.urlsafe_b64encode(
            bytes(door.name, string_encoding)),
            string_encoding
        )
    else:
        return None

    return os.path.join(data_dir, filename)


def load_collection():
    global current

    data_dir = get_doors_data_dir()

    if (os.path.isdir(data_dir)) and (os.path.exists(data_dir)):
        for filename in os.listdir(data_dir):
            path = os.path.join(data_dir, filename)
            door = load_door(path)

            if not door:
                continue

            collection.add_door(door)
    
    doors = collection.list_doors()
    current = doors[0] if len(doors) > 0 else None
    
    collection.select_door(current)
    collection.reload_door()


def store_collection():
    data_dir = get_doors_data_dir()

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.isdir(data_dir):
        return
    
    for door in collection.list_doors():
        path = door_get_path(door)

        if not path:
            continue

        store_door(path, door)


idle_task = None
cancellable = None


def new_door_dialog(window):
    builder = Gtk.Builder()
    builder.add_from_file("new_door_dialog.ui")

    dialog = builder.get_object("dialog")

    cancel_button = builder.get_object("cancel_button")
    confirm_button = builder.get_object("confirm_button")

    name_entry = builder.get_object("name_entry")
    address_entry = builder.get_object("address_entry")
    port_spinbutton = builder.get_object("port_spinbutton")
    open_entry = builder.get_object("open_entry")
    close_entry = builder.get_object("close_entry")
    state_entry = builder.get_object("state_entry")
    locked_entry = builder.get_object("locked_entry")
    unlocked_entry = builder.get_object("unlocked_entry")

    door = Door()

    def change_name(entry):
        door.name = str(entry.get_text())
    
    def change_address(entry):
        door.address = str(entry.get_text())
    
    def change_port(spinbutton):
        door.port = int(spinbutton.get_value())
    
    def change_open_cmd(entry):
        door.open_cmd = str(entry.get_text())
    
    def change_close_cmd(entry):
        door.close_cmd = str(entry.get_text())
    
    def change_state_cmd(entry):
        door.state_cmd = str(entry.get_text())
    
    def change_locked_val(entry):
        door.locked_val = str(entry.get_text())
    
    def change_unlocked_val(entry):
        door.unlocked_val = str(entry.get_text())

    def cancel(_button):
        dialog.destroy()
    
    def confirm(_button):
        global collection

        collection.add_door(door)
        collection.select_door(door)

        dialog.destroy()
    
    name_entry.set_text(str(door.name))
    address_entry.set_text(str(door.address))
    port_spinbutton.set_value(int(door.port))
    open_entry.set_text(str(door.open_cmd))
    close_entry.set_text(str(door.close_cmd))
    state_entry.set_text(str(door.state_cmd))
    locked_entry.set_text(str(door.locked_val))
    unlocked_entry.set_text(str(door.unlocked_val))

    cancel_button.connect("clicked", cancel)
    confirm_button.connect("clicked", confirm)

    name_entry.connect("changed", change_name)
    address_entry.connect("changed", change_address)
    port_spinbutton.connect("changed", change_port)
    open_entry.connect("changed", change_open_cmd)
    close_entry.connect("changed", change_close_cmd)
    state_entry.connect("changed", change_state_cmd)
    locked_entry.connect("changed", change_locked_val)
    unlocked_entry.connect("changed", change_unlocked_val)

    dialog.set_transient_for(window)
    dialog.show()


def edit_door_dialog(window):
    builder = Gtk.Builder()
    builder.add_from_file("edit_door_dialog.ui")

    dialog = builder.get_object("dialog")

    cancel_button = builder.get_object("cancel_button")
    confirm_button = builder.get_object("confirm_button")

    name_label = builder.get_object("name_label")
    address_entry = builder.get_object("address_entry")
    port_spinbutton = builder.get_object("port_spinbutton")
    open_entry = builder.get_object("open_entry")
    close_entry = builder.get_object("close_entry")
    state_entry = builder.get_object("state_entry")
    locked_entry = builder.get_object("locked_entry")
    unlocked_entry = builder.get_object("unlocked_entry")

    door = Door()

    door.name = str(current.name)
    door.address = str(current.address)
    door.port = int(current.port)
    door.open_cmd = str(current.open_cmd)
    door.close_cmd = str(current.close_cmd)
    door.state_cmd = str(current.state_cmd)
    door.locked_val = str(current.locked_val)
    door.unlocked_val = str(current.unlocked_val)

    def update_buttons():
        global current

        confirm_button.set_sensitive(not door.equals(current))
    
    def change_address(entry):
        door.address = str(entry.get_text())
        update_buttons()
    
    def change_port(spinbutton):
        door.port = int(spinbutton.get_value())
        update_buttons()
    
    def change_open_cmd(entry):
        door.open_cmd = str(entry.get_text())
        update_buttons()
    
    def change_close_cmd(entry):
        door.close_cmd = str(entry.get_text())
        update_buttons()
    
    def change_state_cmd(entry):
        door.state_cmd = str(entry.get_text())
        update_buttons()
    
    def change_locked_val(entry):
        door.locked_val = str(entry.get_text())
        update_buttons()
    
    def change_unlocked_val(entry):
        door.unlocked_val = str(entry.get_text())
        update_buttons()

    def cancel(_button):
        dialog.destroy()
    
    def confirm(_button):
        global current
        global collection

        current.name = str(door.name)
        current.address = str(door.address)
        current.port = int(door.port)
        current.open_cmd = str(door.open_cmd)
        current.close_cmd = str(door.close_cmd)
        current.state_cmd = str(door.state_cmd)
        current.locked_val = str(door.locked_val)
        current.unlocked_val = str(door.unlocked_val)

        store_collection()
        collection.reload_door()

        dialog.destroy()
    
    name_label.set_text(str(door.name))
    address_entry.set_text(str(door.address))
    port_spinbutton.set_value(int(door.port))
    open_entry.set_text(str(door.open_cmd))
    close_entry.set_text(str(door.close_cmd))
    state_entry.set_text(str(door.state_cmd))
    locked_entry.set_text(str(door.locked_val))
    unlocked_entry.set_text(str(door.unlocked_val))

    update_buttons()

    cancel_button.connect("clicked", cancel)
    confirm_button.connect("clicked", confirm)

    address_entry.connect("changed", change_address)
    port_spinbutton.connect("changed", change_port)
    open_entry.connect("changed", change_open_cmd)
    close_entry.connect("changed", change_close_cmd)
    state_entry.connect("changed", change_state_cmd)
    locked_entry.connect("changed", change_locked_val)
    unlocked_entry.connect("changed", change_unlocked_val)

    dialog.set_transient_for(window)
    dialog.show()


def about_dialog(window):
    builder = Gtk.Builder()
    builder.add_from_file("about_door_dialog.ui")

    dialog = builder.get_object("dialog")

    close_button = builder.get_object("close_button")

    def close(_button):
        dialog.destroy()

    dialog.set_version(__version__)

    close_button.connect("clicked", close)

    dialog.set_transient_for(window)
    dialog.show()


def door_row(door):
    builder = Gtk.Builder()
    builder.add_from_file("door_row.ui")

    row = builder.get_object("row")

    name_label = builder.get_object("name_label")

    name_label.set_text(door.name)

    row.door = door
    door.widget = row

    return row


def main():
    builder = Gtk.Builder()
    builder.add_from_file("door.ui")

    window = builder.get_object("window")
    window.set_application(app)

    window.connect("destroy", Gtk.main_quit)
    
    header_bar = builder.get_object("header_bar")
    menu_flap = builder.get_object("menu_flap")

    menu_button = builder.get_object("menu_button")
    settings_button = builder.get_object("settings_button")

    add_button = builder.get_object("add_button")
    search_entry = builder.get_object("search_entry")
    remove_button = builder.get_object("remove_button")

    doors_listbox = builder.get_object("doors_listbox")

    about_button = builder.get_object("about_button")
    version_label = builder.get_object("version_label")

    refresh_button = builder.get_object("refresh_button")
    open_button = builder.get_object("open_button")
    close_button = builder.get_object("close_button")
    status_button = builder.get_object("status_button")
    cancel_button = builder.get_object("cancel_button")

    state_stack = builder.get_object("state_stack")
    error_label = builder.get_object("error_label")
    status_label = builder.get_object("status_label")

    def task_search_complete(ps, res, user_data):
        global cancellable
        
        if ps.get_successful():
            set_state("ready")
        else:
            set_state("error")

        cancellable = None

    def task_searching():
        global current
        global idle_task
        global cancellable

        if cancellable is None:
            cancellable = Gio.Cancellable.new()

        ps = Gio.Subprocess.new(["ping", "-c", "1", str(current.address)], Gio.SubprocessFlags.STDOUT_PIPE)
        ps.wait_async(cancellable, task_search_complete, None)

        idle_task = None
        return False

    def task_open_complete(ps, res, user_data):
        global current
        global cancellable
        
        result = None

        if ps.get_successful():
            success, buffer, bytes_read = ps.get_stdout_pipe().read_all(cancellable)

            if success:
                result = str(buffer, string_encoding)

        if result == str(current.unlocked_val):
            set_state("ready")
        else:
            set_state("error", result)

        cancellable = None

    def task_open():
        global current
        global idle_task
        global cancellable

        if cancellable is None:
            cancellable = Gio.Cancellable.new()

        ps = Gio.Subprocess.new(["ssh", "%s@%s" % (str(current.open_cmd), str(current.address))], Gio.SubprocessFlags.STDOUT_PIPE)
        ps.wait_async(cancellable, task_open_complete, None)

        idle_task = None
        return False
    
    def task_close_complete(ps, res, user_data):
        global current
        global cancellable
        
        result = None

        if ps.get_successful():
            success, buffer, bytes_read = ps.get_stdout_pipe().read_all(cancellable)

            if success:
                result = str(buffer, string_encoding)

        if result == str(current.locked_val):
            set_state("ready")
        else:
            set_state("error", result)

        cancellable = None
    
    def task_close():
        global current
        global idle_task
        global cancellable

        if cancellable is None:
            cancellable = Gio.Cancellable.new()

        ps = Gio.Subprocess.new(["ssh", "%s@%s" % (str(current.close_cmd), str(current.address))], Gio.SubprocessFlags.STDOUT_PIPE)
        ps.wait_async(cancellable, task_close_complete, None)
        
        idle_task = None
        return False
    
    def task_reading_complete(ps, res, user_data):
        global current
        global cancellable

        result = None

        if ps.get_successful():
            success, buffer, bytes_read = ps.get_stdout_pipe().read_all(cancellable)

            if success:
                result = str(buffer, string_encoding)

        if (result == str(current.locked_val)) or (result == str(current.unlocked_val)):
            set_state("status", result)
        else:
            set_state("error", result)

        cancellable = None
    
    def task_reading():
        global current
        global idle_task
        global cancellable

        if cancellable is None:
            cancellable = Gio.Cancellable.new()

        ps = Gio.Subprocess.new(
            ["ssh", "%s@%s" % (str(current.state_cmd), str(current.address))],
            Gio.SubprocessFlags.STDOUT_PIPE
        )
        
        ps.wait_async(cancellable, task_reading_complete, None)

        idle_task = None
        return False

    def set_state(state, msg=None):
        global idle_task
        global cancellable

        if state == "ready":
            settings_button.set_sensitive(True)
            refresh_button.set_sensitive(True)
            open_button.set_sensitive(True)
            close_button.set_sensitive(True)
            status_button.set_sensitive(True)
            cancel_button.set_sensitive(False)
        elif state == "status":
            settings_button.set_sensitive(True)
            refresh_button.set_sensitive(True)
            open_button.set_sensitive(True)
            close_button.set_sensitive(True)
            status_button.set_sensitive(True)
            cancel_button.set_sensitive(False)

            if msg is not None:
                status_label.set_text(str(msg))
        elif state == "none":
            settings_button.set_sensitive(False)
            refresh_button.set_sensitive(False)
            open_button.set_sensitive(False)
            close_button.set_sensitive(False)
            status_button.set_sensitive(False)
            cancel_button.set_sensitive(False)
        elif state == "error":
            settings_button.set_sensitive(True)
            refresh_button.set_sensitive(True)
            open_button.set_sensitive(False)
            close_button.set_sensitive(False)
            status_button.set_sensitive(False)
            cancel_button.set_sensitive(False)

            if msg is not None:
                error_label.set_text(str(msg))
        else:
            settings_button.set_sensitive(False)
            refresh_button.set_sensitive(False)
            open_button.set_sensitive(False)
            close_button.set_sensitive(False)
            status_button.set_sensitive(False)
            cancel_button.set_sensitive(True)

        if cancellable is not None:
            cancellable.cancel()
            cancellable = None

        if idle_task is not None:
            GLib.source_remove(idle_task)

        state_stack.set_visible_child_name(state)
        
        if state == "searching":
            idle_task = GLib.idle_add(task_searching)
        elif state == "opening":
            idle_task = GLib.idle_add(task_open)
        elif state == "closing":
            idle_task = GLib.idle_add(task_close)
        elif state == "reading":
            idle_task = GLib.idle_add(task_reading)
        else:
            idle_task = None
    
    def row_get_door(row):
        if not row:
            return None

        children = row.get_children()
        child = None

        if len(children) > 0:
            child = children[0]
        
        return child.door if child else None
    
    def door_get_row(door):
        if not door:
            return None
        
        widget = door.widget

        return widget.get_parent() if widget else None
    
    def window_select_door(door):
        row = door_get_row(door)

        if not row:
            doors_listbox.unselect_all()
            return
        
        doors_listbox.select_row(row)
    
    def window_list_doors():
        children = doors_listbox.get_children()
        doors = []

        for row in children:
            door = row_get_door(row)

            if not door:
                continue

            doors.append(door)

        return doors
    
    def window_add_door(door):
        widget = door_row(door)

        if not widget:
            return
        
        doors_listbox.add(widget)
        store_collection()
    
    def window_reload_door():
        global current

        if current:
            set_state("searching")
        else:
            set_state("none")
        
        menu_flap.set_reveal_flap(False)
    
    def window_remove_door(door):
        row = door_get_row(door)

        if not row:
            return
        
        doors_listbox.remove(row)
        row.destroy()

        path = door_get_path(door)

        if not path:
            return
        
        delete_door(path)
        current = None

        window_reload_door()

    collection.select_door = window_select_door
    collection.list_doors = window_list_doors
    collection.add_door = window_add_door
    collection.reload_door = window_reload_door
    collection.remove_door = window_remove_door

    def on_menu(_button):
        menu_flap.set_reveal_flap(not menu_flap.get_reveal_flap())
    
    def on_settings(_button):
        edit_door_dialog(window)

    def add_door(_button):
        new_door_dialog(window)
    
    def search_door(entry):
        needle = entry.get_text()

        def filter_func(row):
            if row == doors_listbox.get_selected_row():
                return True

            door = row_get_door(row)

            if not door:
                return False

            return needle in door.name

        doors_listbox.set_filter_func(filter_func)

    def remove_door(_button):
        row = doors_listbox.get_selected_row()
        door = row_get_door(row)

        if not door:
            return
        
        window_remove_door(door)

    def select_door(_listbox, row):
        global current

        door = row_get_door(row)

        remove_button.set_sensitive(not door is None)
        current = door

        window_reload_door()

    def refresh(_button):
        set_state("searching")

    def open_door(_button):
        set_state("opening")

    def close_door(_button):
        set_state("closing")
    
    def read_status(_button):
        set_state("reading")

    def cancel(_button):
        set_state("error")

    def about_info(_button):
        about_dialog(window)

    version_label.set_text(__version__)
    
    menu_button.connect("clicked", on_menu)
    settings_button.connect("clicked", on_settings)

    add_button.connect("clicked", add_door)
    search_entry.connect("changed", search_door)
    remove_button.connect("clicked", remove_door)

    doors_listbox.connect("row-selected", select_door)

    refresh_button.connect("clicked", refresh)
    open_button.connect("clicked", open_door)
    close_button.connect("clicked", close_door)
    status_button.connect("clicked", read_status)
    cancel_button.connect("clicked", cancel)

    about_button.connect("clicked", about_info)

    set_state("none")

    load_collection()

    window.show()
    Gtk.main()

def init_style():
    screen = Gdk.Screen.get_default()

    provider = Gtk.CssProvider.new()
    provider.load_from_data(css)

    Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def activate_main(_app):
    init_style()
    main()

if __name__ == "__main__":
    app.connect("activate", activate_main)
    app.run()

