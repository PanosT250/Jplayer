from abc import ABC, abstractmethod
from typing import List, Optional


class I_player(ABC):
    current: str
    songs: List[str]

    @abstractmethod
    def play(self) -> None:
        """Start playback"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop playback"""
        pass
    
class I_play_next_song_strategy(ABC):
    @abstractmethod
    def get_next_song(self, player: I_player) -> str:
        pass

class I_commmand_input_strategy(ABC):
    @abstractmethod
    def get_command(self) -> str:
        pass