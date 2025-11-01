import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from pygame import mixer
from typing import List
from interfaces import I_play_next_song_strategy, I_commmand_input_strategy, I_player
from helpers import play_next_in_queue, play_random_in_queue, play_selected_song, SongNotFoundError


class Jplayer(I_player):
    songs: List[str] = []
    song_selection_strategy: I_play_next_song_strategy
    playlistActive: bool = False
    current: str
    directory: str

    def __init__(self) -> None:
        # TODO: Load playlists

        mixer.init()
        # TODO: make this a separate module or class
        self.directory = "./songs/"
        self.load_all_songs(self.get_all_songs())

        self.song_selection_strategy = play_next_in_queue()

        self.shuffle()

        # Test validity
        # for s in self.songs:
        #     if s.endswith("_fixed.mp3"):
        #         mixer.music.load(s)
        #         self.play()
        #         mixer.music.unload()

        # self.songs.sort()

        # print(self.songs)

    def play_next_song(self):
        self.play_song(self.song_selection_strategy.get_next_song(self))

    def play(self):
        mixer.music.play()

    def stop(self):
        mixer.stop()
    
    def load_all_songs(self, songs) -> None:
        self.songs = songs
        
    def get_all_songs(self):

        songs = []

        for f in os.listdir(self.directory):
            if f.lower().endswith(".mp3"):
                full_path = os.path.abspath(os.path.join(self.directory, f))
                songs.append(os.path.basename(full_path))

        songs.sort()
        return songs

    def shuffle(self) -> bool:
        if isinstance(self.song_selection_strategy, play_next_in_queue):
            self.song_selection_strategy = play_random_in_queue()
            return True
        
        self.song_selection_strategy = play_next_in_queue()
        return False
    
    def play_song(self, song):
        mixer.music.load(song)
        self.current = song
        self.play()
        print(f"Playing: {self.current.removeprefix(self.directory)}")
    
    def search_song(self, input: str):

        try:
            self.play_song(play_selected_song(input, self.directory).get_next_song(self))
        except (SongNotFoundError) as e: 
            print(e)


    def list_songs(self):
        for i, s in enumerate(self.get_all_songs()):
            print(f"{i}. {s}")