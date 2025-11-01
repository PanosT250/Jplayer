from Jplayer import Jplayer

def main():
    player = Jplayer()
    print(len(player.songs))

    player.list_songs()

    player.search_song(input())
    input()


    player.stop()

if __name__ == "__main__":
    main()