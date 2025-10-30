from interfaces import I_play_next_song_strategy, I_player
from pygame import mixer

class play_next_in_queue(I_play_next_song_strategy):

    def get_next_song(self, player: I_player) -> str:

        return player.songs.pop()