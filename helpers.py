from interfaces import I_play_next_song_strategy, I_player
import random, os

class SongNotFoundError(Exception):
    """Raised when a song cannot be found."""
    title: str

    def __init__(self, input) -> None:
        self.input = input

    def __str__(self):
        return f"Could not find song using input: {self.input}"

class play_next_in_queue(I_play_next_song_strategy):

    def get_next_song(self, player: I_player) -> str:

        return player.songs.pop()
    
class play_random_in_queue(I_play_next_song_strategy):

    def get_next_song(self, player: I_player) -> str:

        idx = random.randrange(len(player.songs))
        return player.songs.pop(idx)
    
class play_selected_song(I_play_next_song_strategy):

    input: str
    directory: str

    def __init__(self, input: str, directory: str) -> None:

        self.input = input
        self.directory = directory

    def get_next_song(self, player: I_player) -> str:

        idx = -1

        if self.input.isdigit():
            idx = int(self.input)
        else:
            lower_input = self.input.lower()
            for i, s in enumerate(player.songs):
                s = s.lower()
                if lower_input in [s, s.removesuffix(".mp3")]:
                    idx = i
                    break
        
        if idx in range(len(player.songs)):
            song = player.get_all_songs()[idx]
            player.songs.remove(song)
        else:
            raise SongNotFoundError(self.input)

        
        return song
    