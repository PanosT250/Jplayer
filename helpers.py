from interfaces import I_play_next_song_strategy, I_player
import random

class play_next_in_queue(I_play_next_song_strategy):

    def get_next_song(self, player: I_player) -> str:

        return player.songs.pop()
    
class play_random_in_queue(I_play_next_song_strategy):

    def get_next_song(self, player: I_player) -> str:

        idx = random.randrange(len(player.songs))
        return player.songs.pop(idx)