from Jplayer import Jplayer
from helpers import play_next_in_queue

def main():
    player = Jplayer()

    player.playNextSong()

    print(f"Playing: {player.get_current_song()}")

    input()

    player.stop()

if __name__ == "__main__":
    main()