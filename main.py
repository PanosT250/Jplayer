from Jplayer import Jplayer
import threading
from helpers import audio_event_processor

def main():
    player = Jplayer()

    player.list_songs()

    player.listen_for_command()
    

if __name__ == "__main__":
    main()