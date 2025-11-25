from interfaces import I_play_next_song_strategy, I_player, I_commmand_input_strategy
import random, time
from audio_event_module import audio_event_module
import sounddevice as sd

class SongNotFoundError(Exception):
    """Raised when a song cannot be found."""
    title: str

    def __init__(self, input) -> None:
        self.input = input

    def __str__(self):
        return f"Could not find song using input: {self.input}"

class play_next_in_queue(I_play_next_song_strategy):

    def get_next_song(self, player: I_player) -> int:

        return player.current + 1 if player.current is not None else 0
    
class play_random_in_queue(I_play_next_song_strategy):

    def get_next_song(self, player: I_player) -> int:

        idx = random.randrange(len(player.songs))
        return idx
    
class play_selected_song(I_play_next_song_strategy):


    # TODO: rework this
    input: str
    directory: str

    def __init__(self, input: str, directory: str) -> None:

        self.input = input
        self.directory = directory

    def get_next_song(self, player: I_player) -> int:

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
        
        if 0 <= idx < len(player.songs):
            print(player.current)
            new_idx = ((player.current or 0) + 1) % len(player.songs)
            song = player.songs.pop(idx)
            player.songs.insert(new_idx, song)
        else:
            raise SongNotFoundError(self.input)
        
        return new_idx
    
class terminal_command_processor(I_commmand_input_strategy):

    player: I_player
    def __init__(self, player):
        self.player = player
    
    def listen_for_command(self):
        in_str = ""

        while in_str not in ["stop", "exit"]:
            in_str = input("Enter command: ")

            split_input = in_str.split(" ")
            command = split_input[0]
            args = split_input[1:]

            self.player.process_command(command, args)

class audio_event_processor(I_commmand_input_strategy):

    player: I_player
    def __init__(self, player):
        self.player = player