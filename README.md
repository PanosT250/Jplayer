# JPlayer - Python Music Player

JPlayer is a simple command-line music player written in Python using the VLC library. It allows you to play and manage your music collection effortlessly. You can play, pause, skip tracks, control volume, and more, all from the command line.

## Features

- Play MP3 music files from your local directory.
- Pause and resume playback.
- Skip to the next track in your playlist.
- Download songs from YouTube and add them to your playlist.
- Remove unwanted songs from your playlist.
- Shuffle your playlist for a random listening experience.
- Set the volume of the player.

## Implementation

A custom Jplayer class is used to control the actions of the vlc media player. I used a second thread to monitor the player's state and change the song when it ends. While a better way to do this will surely be possible, I nonetheless wanted to try out python's threading functionality. The helpers.py file contains the JPlayer class and other function such as download which are needed by the project.py file.

## Usage

You can operate this music player with a terminal or by double clicking the project.py file. Type `help` to view the player's commands and run them as you please. The program is designed to store .mp3 files in a folder named `songs` and play them from there. When you are done with the program, type the `exit` command. Thanks for listening!
