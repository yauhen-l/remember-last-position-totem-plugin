# -*- coding: utf-8 -*-

from gi.repository import GObject, Peas # pylint: disable-msg=E0611
import threading
from os.path import expanduser, exists

class StarterPlugin (GObject.Object, Peas.Activatable):
    __gtype_name__ = 'StarterPlugin'

    object = GObject.property (type = GObject.Object)

    def __init__ (self):
        GObject.Object.__init__ (self)
        self.data_path = "%s/.local/share/totem/plugins/remember-last-position/data" % expanduser("~")
        self._totem = None
        self.last_file = ""
        self.last_time = 0

    # totem.Plugin methods

    def do_activate (self):
        self._totem = self.object
        self._totem.connect('file-closed', self.file_closed)
        self._totem.get_main_window().connect('destroy', self.file_closed)
        self._totem.connect('file-has-played', self.file_played)
        self._totem.connect('file-opened', self.file_opened)
        if exists(self.data_path):
            data_file = open(self.data_path, 'r')
            last = data_file.read().split('\n')
            print("Last played is: %s" % last)
            self.last_file = last[0]
            self.last_time = int(last[1])
            data_file.close()

        print("Remember position plugin activated")


    def do_deactivate (self):
        self._totem = None

    def get_current_time(self):
        self.update_time_timer = threading.Timer(3.0, self.get_current_time)
        self.update_time_timer.start()
        self.time = self._totem.get_property('current_time')
        print("Time updated: %d, seekable: %s" % (self.time, self.object.is_seekable()))

    def file_opened(self, to, f):
        print("Opened file: %s" % f)
        if f == self.last_file:
            print("Restoring position in file to %d" % self.last_time)
            print(to.get_current_mrl())
            self.go_to_last_position()

    def go_to_last_position(self):
        if self.object.is_seekable():
            print("Finally go to %d" % self.last_time)
            self._totem.seek_time(self.last_time, False)
        else:
            print("Stream is still not seekable...")
            threading.Timer(0.5, self.go_to_last_position).start()

    def file_closed(self, to):
        if hasattr(self, 'update_time_timer'):
            self.update_time_timer.cancel()
            self.last_file = self.file
            self.last_time = self.time
            self._write_last_time()
        
    def file_played(self, to, path):
        self.get_current_time()
        print("Playng file: %s" % path)
        self.file = path

    def _write_last_time(self):
        print("Saving file position: %s - %d" % (self.last_file, self.last_time))
        data_file = open(self.data_path, 'w')
        data_file.write("%s\n%d" % (self.last_file, self.last_time))
        data_file.close()

