# -*- coding: utf-8 -*-

from gi.repository import GObject, Peas, Totem # pylint: disable-msg=E0611
from threading import Timer
from os.path import expanduser, exists, isfile
from urllib.request import unquote
import csv

class StarterPlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'StarterPlugin'

    object = GObject.property (type = GObject.Object)

    def __init__ (self):
        GObject.Object.__init__ (self)
        self.data_path = "%s/.local/share/totem/plugins/remember-last-position/data-v2" % expanduser("~")
        self._totem = None
        self.last_file = ""
        self.last_time = 0
        self.last_files = []

    # totem.Plugin methods

    def do_activate (self):
        self._totem = self.object
        self._totem.connect('file-closed', self.file_closed)
        self._totem.get_main_window().connect('destroy', self.file_closed)
        self._totem.connect('file-has-played', self.file_played)
        self._totem.connect('file-opened', self.file_opened)
        if exists(self.data_path):
            with open(self.data_path, 'r') as data_file:
                self.last_files += list(csv.reader(data_file))
                print("Last played is: %s" % self.last_files)
                self.last_file = self.last_files[0][0]
                self.last_time = int(self.last_files[0][1])
                self.restore_last_file_timer = Timer(3.0, self.restore_last_file)
                self.restore_last_file_timer.start()

        print("Remember position plugin activated")

    def do_deactivate (self):
        self._totem = None

    def get_current_time(self):
        self.update_time_timer = Timer(3.0, self.get_current_time)
        self.update_time_timer.start()
        self.time = self._totem.get_property('current_time')
        print("Time updated: %d, seekable: %s" % (self.time, self.object.is_seekable()))

    def file_opened(self, to, f):
        if hasattr(self, 'restore_last_file_timer'):
            self.restore_last_file_timer.cancel()
        print("Opened file: %s" % f)
        position = self._get_position(f)
        if position != None:
            self.last_time = int(position)
            print("Restoring position in file to %d" % self.last_time)
            self.go_to_last_position()

    def go_to_last_position(self):
        if self.object.is_seekable():
            print("Finally go to %d" % self.last_time)
            self._totem.seek_time(self.last_time, False)
        else:
            print("Stream is still not seekable...")
            Timer(0.5, self.go_to_last_position).start()

    def file_closed(self, to):
        if hasattr(self, 'update_time_timer'):
            self.update_time_timer.cancel()
            self.last_file = self.file
            self.last_time = self.time
            self.last_files.insert(0, [self.file, str(self.time)])
            self._write_last_time()
        
    def file_played(self, to, path):
        self.get_current_time()
        print("Playng file: %s" % path)
        self.file = path

    def restore_last_file(self):
        is_exist = exists(unquote(self.last_file.replace('file://', '')))
        print("Restoring file: %s at position %d"  % (self.last_file, self.last_time, ))
        if is_exist:
            self._totem.remote_command(Totem.RemoteCommand.REPLACE, self.last_file)

    def _write_last_time(self):
        print("Saving file position: %s - %d" % (self.last_file, self.last_time))
        with open(self.data_path, 'w') as data_file:
            w = csv.writer(data_file)
            w.writerows(self.last_files[:10])

    def _get_position(self, f):
        files = self.last_files[:]
        files.reverse()
        return dict(files).get(f)

