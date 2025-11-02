from Jplayer import Jplayer

def main():
    player = Jplayer()
    print(len(player.songs))

    player.list_songs()

    in_str = ""

    while in_str not in ["stop", "exit"]:
        in_str = input("Enter command: ")
        player.process_command(in_str)

    player.stop()

if __name__ == "__main__":
    main()