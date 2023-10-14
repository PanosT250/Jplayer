import vlc
import sys, os
from threading import Thread
from helpers import download, JPlayer, help_msg


def playstate(q):
    if command := q.split()[0]:
        if command == 'list' or command == 'ls':
            print()
            for i, song in enumerate(jplayer.songs):
                print(str(i + 1) + '. ' + song.replace('.mp3', ''))
            print()            
        elif command == 'p':
            jplayer.player.pause()
        elif command == 'h' or command == 'help':
            print(help_msg)
        elif command == 'c':
            jplayer.player.play()
        elif command == 'skip':
            jplayer.new_song()
        elif command == 'exit':
            prog_end()
        elif command == 'rm' or command == 'remove':
            if args := q.replace(f'{command} ', '').split(','):
                for arg in args:
                    arg = arg.capitalize().strip()
                    if os.path.exists(f'./songs/{arg}.mp3'):
                        os.remove('./songs/' + arg + '.mp3')
                        print(f'Deleted: {arg}')
                    else:
                        print(f'{arg} not found')
                jplayer.load_songs()
            else:
                print('No songs found')
        elif command == 'shuffle':
            jplayer.shuffle = not jplayer.shuffle
            print('Shuffle is', 'on' if jplayer.shuffle else 'off')
        elif command == 's' or command == 'song':
            jplayer.request_song(' '.join(q.split()[1:]).capitalize())
        elif command == 'v' or command == 'vol' or command == 'volume':
            try:
                jplayer.player.audio_set_volume(int(q.split()[1]))
            except (ValueError, IndexError):
                print('Usage: vol <percentage>')
        elif command in ['dl', 'download', 'down']:
            download(input('Youtube url: '))
            jplayer.load_songs()
        else:
            print('Unavailable command')
            return 1


def listen_song():
    global jplayer

    while not jplayer.songs:
        print("Song folder empty, please download a song:")
        playstate('download')
        jplayer.load_songs()

    jplayer.new_song()

    while True:
        try:
            playstate(input(''))
        except (OSError, KeyboardInterrupt, EOFError):
            return


def check_ended():

    while True:
        try:
            if jplayer.player.get_state() == vlc.State.Ended:
                jplayer.new_song()
        except (OSError, KeyboardInterrupt):
            return


def main():
    t1 = Thread(target=listen_song)
    t1.start()
    
    check_ended()

def prog_end():
    jplayer.player.release()
    jplayer.instance.release()
    print('Thanks for listening!')
    sys.exit(0)


# Init player
jplayer = JPlayer()

if __name__ == '__main__':
    main()