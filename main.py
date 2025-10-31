from Jplayer import Jplayer

def main():
    player = Jplayer()
    print(len(player.songs))

    player.playNextSong()
    input()


    player.stop()

if __name__ == "__main__":
    main()