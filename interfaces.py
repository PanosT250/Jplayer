from abc import ABC, abstractmethod
from typing import List, Optional


class I_player(ABC):

    @property
    @abstractmethod
    def current(self) -> Optional[int]:
        """Index of current song""" 
        pass

    songs: List[str]

    @abstractmethod
    def play(self) -> None:
        """Start playback"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop playback"""
        pass

    @abstractmethod
    def get_all_songs(self) -> List[str]:
        """Get all songs"""
        pass
    
class I_play_next_song_strategy(ABC):
    @abstractmethod
    def get_next_song(self, player: I_player) -> int:
        pass

class I_commmand_input_strategy(ABC):
    @abstractmethod
    def get_command(self) -> str:
        pass