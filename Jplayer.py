import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from pygame import mixer
from typing import List
from interfaces import I_play_next_song_strategy, I_commmand_input_strategy, I_player
from helpers import play_next_in_queue, play_random_in_queue, play_selected_song, SongNotFoundError


class Jplayer(I_player):

    # use this like a list to have prev commands
    songs: List[str] = []
    song_selection_strategy: I_play_next_song_strategy
    playlistActive: bool = False
    current: str
    playing: bool
    directory: str

    def __init__(self) -> None:
        # TODO: Load playlists

        mixer.init()
        # TODO: make this a separate module or class
        self.directory = "./songs/"
        self.load_all_songs(self.get_all_songs())

        self.song_selection_strategy = play_next_in_queue()

        # self.shuffle()
        self.playing = False

    def play_next_song(self):
        self.play_song(f"{self.song_selection_strategy.get_next_song(self)}")

    def play(self):
        mixer.music.play()
        self.playing = True

    def stop(self):
        mixer.stop()
        self.playing = False
    
    def load_all_songs(self, songs) -> None:
        self.songs = songs
        
    def get_all_songs(self):

        songs = []

        for f in os.listdir(self.directory):
            if f.lower().endswith(".mp3"):
                full_path = os.path.abspath(os.path.join(self.directory, f))
                songs.append(os.path.basename(full_path))

        return songs

    def shuffle(self) -> bool:
        if isinstance(self.song_selection_strategy, play_next_in_queue):
            self.song_selection_strategy = play_random_in_queue()
            return True
        
        self.song_selection_strategy = play_next_in_queue()
        return False
    
    def play_song(self, song):
        mixer.music.load(f"{self.directory}{song}")
        self.current = song
        self.play()
        print(f"Playing: {self.current.removeprefix(self.directory)}")
    
    def search_song(self, input: str):

        self.stop()

        try:
            self.play_song(play_selected_song(input, self.directory).get_next_song(self))
        except (SongNotFoundError) as e: 
            print(e)

    def list_songs(self, queue=False):

        if not queue:
            songs = self.get_all_songs()
        else:
            songs = self.songs

        for i, s in enumerate(songs):
            print(f"{i}. {s}")

    def process_command(self, in_str):

        split_input = in_str.split(" ")
        command = split_input[0]
        args = split_input[1:]
        has_args = len(args) > 0

        if command in ["p"]:
            self.play() if not self.playing else self.stop()
        elif command in ["play"]:
            self.play()
        elif command in ["pause"]:
            self.stop()
        elif command in ["l", "list", "all", "ls"]:
            if has_args and args[0] in ["queue", "q"]:
                self.list_songs(queue=True)
            else:
                self.list_songs()

        elif command in ["song", "search", "sn", "sname"]:

            if has_args:
                self.search_song(args[0])

        elif command in ["shuffle"]:
            print(f"Shuffle is {"on" if self.shuffle() else "off"}")

        elif command in ["skip", "next"]:
            self.play_next_song()

        elif command in ["reload"]:
            self.load_all_songs(self.get_all_songs())

        #TODO: help, playlist, download, stream, voice operation enable/disable