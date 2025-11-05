import os, json, sys
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from pygame import mixer
from typing import List
from interfaces import I_play_next_song_strategy, I_commmand_input_strategy, I_player
from helpers import play_next_in_queue, play_random_in_queue, play_selected_song, SongNotFoundError

SETTINGS_FILE_NAME: str = "settings.json"
DEFAULT_SETTINGS_FILE_NAME: str = "default_settings.json"



def settings_dec(func):
    def wrapper(*args, **kwargs):
        if not os.path.exists(SETTINGS_FILE_NAME):
            default_settings = open(DEFAULT_SETTINGS_FILE_NAME).read()
            with open(SETTINGS_FILE_NAME, "w") as f:
                f.write(default_settings)

        func(*args, **kwargs)

    return wrapper

@settings_dec
def change_setting(key: str, val):
    try:
        with open(SETTINGS_FILE_NAME, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        sys.exit("Settings file not found")

    data[key] = val

    # Save back to file
    with open(SETTINGS_FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Set {key} = {val} in {SETTINGS_FILE_NAME}")

class Jplayer(I_player):

    # use this like a list to have prev commands
    songs: List[str] = []
    song_selection_strategy: I_play_next_song_strategy
    playlistActive: bool = False
    playing: bool
    directory: str

    @property
    def current(self):
        return self._current
    
    @current.setter
    def current(self, value):
        
        self._current = value % len(self.songs)

    @settings_dec
    def load_settings(self):
        with open(SETTINGS_FILE_NAME, "r") as f:
            data = json.load(f)
            self.directory = data["directory"]

    def __init__(self) -> None:
        # TODO: Load playlists

        self.load_settings()

        self._current = None
        mixer.init()
        # TODO: make this a separate module or class
        self.load_songs(self.get_all_songs())

        self.song_selection_strategy = play_next_in_queue() # maybe change this through startup settings

        self.playing = False

        idx = self.song_selection_strategy.get_next_song(self)

        self.load(idx)

    def play_next_song(self):
        self.load(self.song_selection_strategy.get_next_song(self))
        self.play()

    def play(self):
        mixer.music.play()
        print(self.current)
        if self.current != None:
            print(f"Playing: {self.songs[self.current].removeprefix(self.directory)}")
            self.playing = True
        else:
            raise ValueError("Player current song not set")

    def stop(self):
        mixer.stop()
        print(f"Paused")
        self.playing = False
    
    def load_songs(self, songs) -> None:
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
    
    def load(self, idx):
        self.current = idx
        mixer.music.load(f"{self.directory}{self.songs[self.current]}")
    
    def search_song(self, input: str):

        self.stop()

        try:
            self.load(play_selected_song(input, self.directory).get_next_song(self))
            self.play()
        except (SongNotFoundError) as e: 
            print(e)

    def list_songs(self, queue=False):

        if not queue:
            songs = self.get_all_songs()
        else:
            songs = self.songs

        for i, s in enumerate(songs):
            print(f"{i}. {s}")

    def set_directory(self, dirname: str):
        if os.path.isdir(dirname):
            change_setting("directory", dirname)
            self.directory = dirname
            print(f"Directory is now: {self.directory}")
            self.load_songs(self.get_all_songs())
        else:
            print("Invalid directory, path must begin from jplayer root")

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
            self.load_songs(self.get_all_songs())

        elif command in ["setdir", "directory", "dir"]:
            if has_args:
                self.set_directory(args[0])
            else:
                print("Please provide a valid directory, starting from jplayer root")


        #TODO: help, playlist, download, stream, voice operation enable/disable