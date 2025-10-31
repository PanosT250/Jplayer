import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from pygame import mixer
from typing import List
from interfaces import I_play_next_song_strategy
from helpers import play_next_in_queue, play_random_in_queue


class Jplayer:
    songs: List[str] = []
    song_selection_strategy: I_play_next_song_strategy = play_next_in_queue()
    playlistActive: bool = False
    current: str
    directory: str

    def __init__(self) -> None:
        # TODO: Load playlists

        mixer.init()
        # TODO: make this a separate module or class
        self.directory = "./songs/"
        self.load_all_songs()

        self.shuffle()

        # Test validity
        # for s in self.songs:
        #     if s.endswith("_fixed.mp3"):
        #         mixer.music.load(s)
        #         self.play()
        #         mixer.music.unload()

        # self.songs.sort()

        # print(self.songs)

    def playNextSong(self):

        song = self.song_selection_strategy.get_next_song(self)

        mixer.music.load(song)
        self.current = song
        self.play()
        print(f"Playing: {self.get_current_song()}")


    def play(self):
        mixer.music.play()

    def stop(self):
        mixer.stop()

    def get_current_song(self) -> str:
        return os.path.basename(self.current)
    
    def load_all_songs(self) -> None:
        self.songs.clear()
        for f in os.listdir(self.directory):
            if f.lower().endswith(".mp3"):
                full_path = os.path.abspath(os.path.join(self.directory, f))
                self.songs.append(full_path)

    def shuffle(self) -> bool:
        if isinstance(self.song_selection_strategy, play_next_in_queue):
            self.song_selection_strategy = play_random_in_queue()
            return True
        
        self.song_selection_strategy = play_next_in_queue()
        return False

