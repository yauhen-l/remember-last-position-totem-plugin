# remember-last-position-totem-plugin
Totem video player plugin that restores position in the last played file

# Installation
Put `remember-last-position.plugin` and `remember-last-position.py` files in `~/.local/share/totem/plugins/remember-last-position directory`

Then start Totem and enable "Remember last position" plugin in Plugins view.

# How it works
On video playing it stores file location and current offset in `~/.local/share/totem/plugins/remember-last-position/data` file within 3 seconds delay.

After opening the same file position will be restored.

*_CAUTION!_ 1) For now plugin remembers only one last played file. 2) Not tested on web-sources*

# To do
1. Remember history of more than one file
2. Open last played file on Totem start
