from pytube import YouTube, exceptions
import vlc
import os
import random

# Custom player with personalized methods and instance variables


class JPlayer:
    def __init__(self):
        self.load_songs()

        self.index = 0  # Index of the current song
        self.shuffle = True  # Shuffle mode
        
        self.current = None

        self.instance = vlc.Instance("--no-xlib", "--quiet")
        self.player = self.instance.media_player_new()


    def load_songs(self):
        FOLDER_NAME = "songs" # Check that songs folder exists
        if not (os.path.exists(FOLDER_NAME) and os.path.isdir(FOLDER_NAME)):
            os.mkdir(FOLDER_NAME)
        else:
            self.songs = [song for song in os.listdir(
                'songs') if song.endswith('.mp3')]
            

    def play_song(self):
        if self.current:
            media_path = f'songs/{self.current}'
            media = self.instance.media_new(media_path)
            self.player.set_media(media)
            try:
                self.player.play()
                print('Now playing:', self.current[:-4])
            except Exception as e:
                print(f"Error playing {self.current[:-4]}: {str(e)}")

    def new_song(self):
        if self.shuffle:
            try:
                self.current = random.choice(
                    [song for song in self.songs if song != self.current])
                self.index = self.songs.index(self.current)
            except IndexError:
                pass
        else:
            self.index = self.index + \
                1 if self.index < len(self.songs) - 1 else 0
            self.current = self.songs[self.index]
        self.play_song()

    def request_song(self, req):
        if f'{req}.mp3' in self.songs:
            self.index = self.songs.index(f'{req}.mp3')
            self.current = f'{req}.mp3'
            self.play_song()
        else:
            print(f'Song "{req}" not found in the playlist.')


def download(video_url):

    try:
        yt = YouTube(video_url)
    except exceptions.RegexMatchError:
        print('Video not found')
        return 1
    else:
        
        if title := input('Title: '):
            pass
        else:
            title = "Title"
            
        audio_stream = yt.streams.filter(
            only_audio=True, file_extension='mp4').first()

        audio_stream.download(output_path='songs',
                            filename=f'{title.capitalize()}.mp3')
        
        print(f"Successfully downloaded: {title}")
        return 0


commands = {
    'p': 'Pause song',
    'c': 'Continue song',
    'skip': 'Skip to next song',
    'exit': 'Exit player',
    'shuffle': 'Toggle shuffle',
    'song': 'Choose a song to play',
    'vol': 'Change volume',
    'download': 'Download song from Youtube',
    'remove': 'Delete song from songs folder',
    'list': 'View the songs in the songs folder'
}

help_msg = \
'''
Music player with custom commands

List of available commands:

'''

for key in commands:
    help_msg += f'{key}: {commands[key]}\n'
