from abc import ABC, abstractmethod
from typing import List, Optional


class I_player(ABC):

    @property
    @abstractmethod
    def current(self) -> int:
        """Index of current song""" 
        pass

    songs: List[str]

    @abstractmethod
    def play(self) -> None:
        """Resume playback"""
        pass

    @abstractmethod
    def pause(self) -> None:
        """Pause playback"""
        pass

    @abstractmethod
    def get_all_songs(self) -> List[str]:
        """Get all songs"""
        pass

    @abstractmethod
    def process_command(self, command: str, args: List[str] = []) -> None:
        """Get all songs"""
        pass
    
class I_play_next_song_strategy(ABC):
    @abstractmethod
    def get_next_song(self, player: I_player) -> int:
        pass

class I_commmand_input_strategy(ABC):

    player: I_player
    @abstractmethod
    def listen_for_command(self) -> None:
        pass