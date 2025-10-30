from abc import ABC, abstractmethod
from typing import List

class I_play_next_song_strategy(ABC):
    @abstractmethod
    def get_next_song(self, player) -> str:
        pass

class I_player(ABC):
    @property
    @abstractmethod
    def songs(self) -> List[str]:
        """A list of loaded songs"""
        pass

    @abstractmethod
    def play(self) -> None:
        """Start playback"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop playback"""
        pass