# Remember Last Position Totem Plugin
Totem video player plugin that starts a video at the location you paused
it last time it played.
It also supports automatically continue to play the last video when
Totem starts.

# Installation
Create a plugin folder in `~/.local/share/totem/plugins/<plugin-folder>`,
and put all the plugin files there:

        remember-last-position.plugin
        remember-last-position.py
        remember-last-position.conf

Then start Totem and enable "Remember last position" plugin
in Plugins view.

# How it works
On video playing it stores file path and current video location offset
in `remember-last-position.pydata` at the plugin folder.

After opening the same file, its location will be restored.

If load-on-start feature is enabled (disabled by default),
on Totem start it will waits 5 seconds (default), and then opens the
last played file and restores its video location.

*_CAUTION!_ Not tested on web-sources*

# Tuning
It is possible to tune the plugin parameters via
`remember-last-position.conf` file:

+ `load-on-start`: Explained above (true, false).
+ `load-on-start-delay`: The time to wait for the video to start (seconds).
+ `history-length`: How many files will be stored (integer).
+ `update-interval`: Update the video position on interval (seconds).

## Special Thanks:
Thanks to Asanka's Weblog for quick start:
http://asanka-abeyweera.blogspot.com/2012/03/writing-plugins-for-totem-movie-player.html
