import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from pygame import mixer
from typing import List
from interfaces import I_play_next_song_strategy
from helpers import play_next_in_queue


class Jplayer:
    songs: List[str] = []
    strategy: I_play_next_song_strategy = play_next_in_queue()
    playlistActive: bool = False
    current: str

    def __init__(self) -> None:
        # TODO: Load playlists and songs

        # TODO: make this a separate module or class
        mixer.init()
        directory = "./songs/"

        for f in os.listdir(directory):
            if f.lower().endswith(".mp3"):
                full_path = os.path.abspath(os.path.join(directory, f))
                self.songs.append(full_path)

    def playNextSong(self):
        song = self.strategy.get_next_song(self)
        mixer.music.load(song)
        self.current = song
        self.play()

    def play(self):
        mixer.music.play()

    def stop(self):
        mixer.stop()

    def get_current_song(self) -> str:
        
        return os.path.basename(self.current)
