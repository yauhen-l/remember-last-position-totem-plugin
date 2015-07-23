# remember-last-position-totem-plugin
Totem video player plugin that restores position in the last played file

# Installation
Put `remember-last-position.plugin` and `remember-last-position.py` files in `~/.local/share/totem/plugins/remember-last-position directory`

Then start Totem and enable "Remember last position" plugin in Plugins view.

# How it works
On Totem start it waits 3 seconds and then opens last played file and restores position in it.

On video playing it stores file location and current offset in `~/.local/share/totem/plugins/remember-last-position/data` file within 3 seconds delay.

After opening the same file position will be restored.

*_CAUTION!_ 1) For now plugin remembers only one last played file. 2) Not tested on web-sources*

# To do
Remember history of more than one file

## Thanks to Asanka's Weblog for quick start:
http://asanka-abeyweera.blogspot.com/2012/03/writing-plugins-for-totem-movie-player.html
