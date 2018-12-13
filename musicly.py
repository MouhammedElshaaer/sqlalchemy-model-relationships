import vlc
import time
import random
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicly.db'
db = SQLAlchemy(app)
storage_path = "songs/"

"""************************************************************************************************************
                                                Models
************************************************************************************************************"""

playlist_song = db.Table('playlist_song',
                         db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
                         db.Column('song_id', db.Integer, db.ForeignKey('song.id')))


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    # one-to-many
    songs = db.relationship('Song', secondary=playlist_song, backref='playlists', lazy='dynamic')

    def __repr__(self):
        return "PlayList: {}    Songs: {}\n".format(self.title, self.songs.count())

    def __str__(self):
        return "PlayList: {}    Songs: {}\n".format(self.title, self.songs.count())


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # songs_number = db.Column(db.Integer)

    # many-to-one
    band_id = db.Column(db.Integer, db.ForeignKey('band.id', ondelete='cascade'), nullable=True, default=None)

    # many-to-one
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete='cascade'), nullable=True, default=None)

    # one-to-many
    songs = db.relationship('Song', backref='album', lazy=True)

    def __repr__(self):
        return "Album: {}   Songs: {}\n".format(self.title, len(self.songs))

    def __str__(self):
        return "Album: {}   Songs: {}\n".format(self.title, len(self.songs))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    album_release_date = db.Column(db.String(20), nullable=False)
    genres = db.Column(db.String(20), nullable=False)
    lyrics = db.Column(db.String(20), nullable=False)
    length = db.Column(db.String(20), nullable=False)

    # many-to-one
    band_id = db.Column(db.Integer, db.ForeignKey('band.id', ondelete='cascade'), nullable=True, default=None)

    # many-to-one
    album_id = db.Column(db.Integer, db.ForeignKey('album.id', ondelete='cascade'), nullable=True, default=None)

    # many-to-one
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete='cascade'), nullable=True, default=None)

    def __repr__(self):
        return "Song: {}    Genres: {}  Length: {}\n".format(self.name, self.genres, self.length)

    def __str__(self):
        return "Song: {}    Genres: {}  Length: {}\n".format(self.name, self.genres, self.length)


class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    # one-to-many
    albums = db.relationship('Album', backref='band', lazy=True)

    # one-to-many
    songs = db.relationship('Song', backref='band', lazy=True)

    # one-to-many
    artists = db.relationship('Artist', backref='band', lazy=True)

    def __repr__(self):
        return "Band: {}\n".format(self.name)

    def __str__(self):
        return "Band: {}\n".format(self.name)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.String(20), nullable=False)

    # many-to-one
    band_id = db.Column(db.Integer, db.ForeignKey('band.id', ondelete='cascade'), nullable=True, default=None)

    # one-to-many
    songs = db.relationship('Song', backref='artist', lazy=True)

    # one-to-many
    albums = db.relationship('Album', backref='artist', lazy=True)

    def __repr__(self):
        return "Artist: {}      Birth Date: {}\n".format(self.name, self.birth_date)

    def __str__(self):
        return "Artist: {}      Birth Date: {}\n".format(self.name, self.birth_date)


"""************************************************************************************************************
                                                Functions
************************************************************************************************************"""


def header():
    print("""
    ********************************************************
    ****************** Welcome To Musicly ******************
    ********************************************************
    """)


def main_menu():
    print("1. Playlists     2. Artists      3. Albums       4.Library       5. Bands\n")
    footer()


def playlists_view():

    while True:

        print("""
        ********************************************************
        ******************** Playlists Menu ********************
        ********************************************************
        """)

        playlists = get_playlists()

        i = 1
        for playlist in playlists:
            print(str(i), ". ", playlist)
            i += 1

        if i == 1:
            print("** No Playlists **\n")

        print("\n***************************************************************************")
        print("\n************************* Select Playlist To View *************************")
        print("\nA. Add Playlist       D. Delete Playlist       ", end=' ')

        print("P. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        elif user_input == "A":
            add_playlist()
        elif user_input == "D":
            user_input = int(input("Enter Playlist Number To Deleted: "))
            delete_playlist(playlists[int(user_input)-1])
        else:
            playlist_view(playlists[int(user_input)-1])


def playlist_view(playlist):

    while True:

        print("""
        ********************************************************
        ******************** Playlist Songs ********************
        ********************************************************
        """)

        i = 1
        for song in playlist.songs:
            print(str(i), ". ", song)
            i += 1

        if i == 1:
            print("\n** Empty Playlist **\n")
        else:
            print("\n***************************************************************************")
            print("\nSelect a song")
            print("\nS. Shuffle Playlist        D. Delete Song       ", end=' ')

        print("P. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        elif user_input == "D":
            user_input = int(input("Enter Song number To Deleted: ")) - 1
            delete_from_playlist(playlist, playlist.songs[int(user_input) - 1])
        elif user_input == "S":
            shuffle_playlist(playlist)
        else:
            play_song_view(playlist.songs[int(user_input) - 1])


def artists_view():

    while True:

        print("""
        ********************************************************
        ********************* Artists Menu *********************
        ********************************************************
        """)

        artists = get_artists()

        i = 1
        for artist in artists:
            print(str(i), ". ", artist)
            i += 1

        if i == 1:
            print("\n** No Artists **\n")

        print("\n***************************************************************************")
        print("Select an Artist")
        print("\nA. Add Artist       D. Delete Artist       ", end=' ')

        print("P. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        elif user_input == "A":
            add_artist()
        elif user_input == "D":
            user_input = int(input("Enter Artist Number To Deleted: "))
            delete_artist(artists[int(user_input) - 1])
        else:
            artist_view(artists[int(user_input)-1])


def artist_view(artist):
    print("""
    ********************************************************
    ********************* Artist Info **********************
    ********************************************************
    """)

    print(artist)

    user_input = input("S. Artist Songs         A. Artist Albums         P. Previous Menu\n")

    if user_input == "S":
        artist_songs(artist.songs)
    elif user_input == "A":
        artist_albums(artist.albums)


def artist_songs(songs):

    songs_number = len(songs)

    while True:

        print("""
        ********************************************************
        ******************** Artist Songs ********************
        ********************************************************
        """)

        i = 1
        for song in songs:
            print(str(i), ". ", song)
            i += 1

        if i == 1:
            print("\n** Empty Playlist **\n")
        else:
            print("\n***************************************************************************")
            print("\n************************ Select a song To Play ****************************")

        print("\nP. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        else:
            i = int(user_input) - 1
            while True:

                user_input = play_song(songs[i])
                if user_input == "next":
                    i = (i + 1) % songs_number
                    continue
                elif user_input == "prev":
                    i = (i - 1) % songs_number
                    continue
                elif user_input == "repeat":
                    continue
                else:
                    break


def artist_albums(albums):
    while True:

        print("""
        ********************************************************
        ********************* Artist Albums ********************
        ********************************************************
        """)

        i = 1
        for album in albums:
            print(str(i), ". ", album)
            i += 1

        if i == 1:
            print("\n** No Albums **\n")
        else:
            print("\n***************************************************************************")
            print("\n************************ Select An Album To View **************************")

        print("\nP. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        else:
            album_view(album)


def albums_view():

    while True:

        print("""
        ********************************************************
        ************************* Albums ***********************
        ********************************************************
        """)

        albums = get_albums()

        i = 1
        for album in albums:
            print(str(i), ". ", album)
            i += 1

        if i == 1:
            print("\n** No Albums **\n")

        print("\n***************************************************************************")
        print("***************************** Select an Album *******************************")
        print("\nA. Add Album       D. Delete Album       ", end=' ')

        print("P. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        elif user_input == "A":
            add_album()
        elif user_input == "D":
            user_input = int(input("Enter Album Number To Delete: "))
            delete_album(albums[int(user_input) - 1])
        else:
            album_view(albums[int(user_input)-1])


def album_view(album):

    songs_number = len(album.songs)

    while True:

        print("""
        ********************************************************
        ********************** Album Songs *********************
        ********************************************************
        """)

        i = 1
        for song in album.songs:
            print(str(i), ". ", song)
            i += 1

        if i == 1:
            print("\n** Empty Album **\n")
        else:
            print("\n***************************************************************************")
            print("\n************************* Select a song To Play ***************************")

        print("P. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        else:
            i = int(user_input) - 1
            while True:

                user_input = play_song(album.songs[i])
                if user_input == "next":
                    i = (i + 1) % songs_number
                    continue
                elif user_input == "prev":
                    i = (i - 1) % songs_number
                    continue
                elif user_input == "repeat":
                    continue
                else:
                    break


def library_view():

    while True:

        print("""
        ********************************************************
        *********************** Library ************************
        ********************************************************
        """)

        songs = get_songs()
        songs_number = len(songs)

        i = 1
        for song in songs:
            print(str(i), ". ", song)
            i += 1

        if i == 1:
            print("\n** Empty Library **\n")
        else:
            print("\n***************************************************************************")
            print("\n************************ Select a song To Play ****************************")
            print("\nA. Add Song To Playlist       ", end=' ')

        print("P. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        elif user_input == "A":
            user_input = int(input("Enter Song Number To Add: ")) - 1
            add_to_playlist(songs[user_input])
        else:

            i = int(user_input) - 1
            while True:

                user_input = play_song(songs[i])
                if user_input == "next":
                    i = (i+1) % songs_number
                    continue
                elif user_input == "prev":
                    i = (i-1) % songs_number
                    continue
                elif user_input == "repeat":
                    continue
                else:
                    break


def bands_view():
    while True:

        print("""
        ********************************************************
        ********************* Band Menu *********************
        ********************************************************
        """)

        bands = get_bands()

        i = 1
        for band in bands:
            print(str(i), ". ", band)
            i += 1

        if i == 1:
            print("\n** No Bands **\n")

        print("\n***************************************************************************")
        print("Select a Band")
        print("\nS. Songs       A. Albums       ", end=' ')

        print("P. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        elif user_input == "A":
            user_input = input("Enter Band Number: ")
            band_albums(bands[int(user_input)-1].albums)
        elif user_input == "S":
            user_input = input("Enter Band Number: ")
            band_songs(bands[int(user_input)-1].songs)
        else:
            band_view(bands[int(user_input)-1])


def band_albums(albums):
    while True:

        print("""
        ********************************************************
        ********************** Band Albums *********************
        ********************************************************
        """)

        i = 1
        for album in albums:
            print(str(i), ". ", album)
            i += 1

        if i == 1:
            print("\n** No Albums **\n")
        else:
            print("\n***************************************************************************")
            print("\n************************ Select An Album To View **************************")

        print("\nP. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        else:
            album_view(album)


def band_songs(songs):
    songs_number = len(songs)

    while True:

        print("""
            ********************************************************
            ******************** Band Songs ********************
            ********************************************************
            """)

        i = 1
        for song in songs:
            print(str(i), ". ", song)
            i += 1

        if i == 1:
            print("\n** Empty Playlist **\n")
        else:
            print("\n***************************************************************************")
            print("\n************************ Select a song To Play ****************************")

        print("\nP. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        else:
            i = int(user_input) - 1
            while True:

                user_input = play_song(songs[i])
                if user_input == "next":
                    i = (i + 1) % songs_number
                    continue
                elif user_input == "prev":
                    i = (i - 1) % songs_number
                    continue
                elif user_input == "repeat":
                    continue
                else:
                    break


def band_view():
    songs_number = len(album.songs)

    while True:

        print("""
            ********************************************************
            ********************** Album Songs *********************
            ********************************************************
            """)

        i = 1
        for song in album.songs:
            print(str(i), ". ", song)
            i += 1

        if i == 1:
            print("\n** Empty Album **\n")
        else:
            print("\n***************************************************************************")
            print("\n************************* Select a song To Play ***************************")

        print("P. Previous Menu\n")
        print("***************************************************************************\n")

        user_input = input()

        if user_input == "P":
            return
        else:
            i = int(user_input) - 1
            while True:

                user_input = play_song(album.songs[i])
                if user_input == "next":
                    i = (i + 1) % songs_number
                    continue
                elif user_input == "prev":
                    i = (i - 1) % songs_number
                    continue
                elif user_input == "repeat":
                    continue
                else:
                    break


def main():

    while True:

        header()
        main_menu()

        user_input = input()

        if user_input == "1":

            playlists_view()

        elif user_input == "2":

            artists_view()

        elif user_input == "3":

            albums_view()

        elif user_input == "4":

            library_view()

        elif user_input == "5":

            bands_view()

        elif user_input == "Q":
            break


def get_playlists():
    return Playlist.query.all()


def get_artists():
    return Artist.query.all()


def get_bands():
    return Band.query.all()


def get_albums():
    return Album.query.all()


def get_songs():
    return Song.query.all()


def add_playlist():
    db.session.add(
        Playlist(
            title=input("Enter Title: "),
            description=input("Enter Description: ")
        )
    )
    db.session.commit()


def delete_playlist(playlist):
    db.session.delete(playlist)
    db.session.commit()


def add_to_playlist(song):

    print("""
    ********************************************************
    ****************** Choose a Playlist *******************
    ********************************************************
    """)

    playlists = get_playlists()

    i = 1
    for playlist in playlists:
        print(str(i), ". ", playlist)
        i += 1

    if i == 1:
        print("** No Playlists **\n")
    else:
        print("\n***************************************************************************")
        print("Select a playlist")

    print("P. Previous Menu\n")
    print("***************************************************************************\n")

    user_input = input()

    if user_input == "P":
        return
    else:
        playlists[int(user_input) - 1].songs.append(song)
        db.session.commit()


def delete_from_playlist(playlist, song):
    playlist.songs.remove(song)
    db.session.commit()


def add_album():

    _title = input("Enter Title: ")

    user_input = input("Enter A. Artist or B. Band: ")

    _band_id = None
    _artist_id = None

    if user_input == "A":
        _artist_id = browse_artists()
    else:
        _band_id = browse_bands()

    if _band_id == "P" or _artist_id == "P":
        return

    db.session.add(
        Album(
            title=_title,
            band_id=_band_id,
            artist_id=_artist_id
        )
    )
    db.session.commit()


def delete_album(album):
    db.session.delete(album)
    db.session.commit()
    return


def browse_artists():
    print("""
    ********************************************************
    *********************** Artists ************************
    ********************************************************
    """)
    artists = Artist.query.all()
    _artist_id = None
    i = 1
    for artist in artists:
        print(str(i), ". ", artist.name)
        i += 1

    if i == 1:
        print("\n** No Existing Artists **\n")
    else:
        print("\n***************************************************************************")
        print("\n*********************** Select an Artist To Add ***************************")

    print("P. Previous Menu\n")
    print("***************************************************************************\n")

    user_input = input("Artist Number: ")

    if user_input == "P":
        return user_input
    else:
        _artist_id = artists[int(user_input) - 1].id

    return _artist_id


def browse_bands():
    print("""
    ********************************************************
    ************************ Bands *************************
    ********************************************************
    """)
    bands = Band.query.all()
    _band_id = None
    i = 1
    for band in bands:
        print(str(i), ". ", band.name)
        i += 1

    if i == 1:
        print("\n** No Existing Bands **\n")
    else:
        print("\n***************************************************************************")
        print("\n************************** Select a Band To Add ***************************")

    print("P. Previous Menu\n")
    print("***************************************************************************\n")

    user_input = input("Band Number: ")

    if user_input == "P":
        return user_input
    else:
        _band_id = bands[int(user_input) - 1].id

    return _band_id


def browse_albums():
    print("""
        ********************************************************
        ************************ Albums *************************
        ********************************************************
        """)
    albums = Album.query.all()
    _album = None
    i = 1
    for album in albums:
        print(str(i), ". ", album.title)
        i += 1

    if i == 1:
        print("\n** No Existing Albums **\n")
    else:
        print("\n***************************************************************************")
        print("\n************************** Select An Album To Add ***************************")

    print("P. Previous Menu\n")
    print("***************************************************************************\n")

    user_input = input("Album Number: ")

    if user_input == "P":
        return user_input
    else:
        _album = albums[int(user_input) - 1]

    return _album


def add_artist():

    _name = input("Enter Artist Name: ")
    _birth_date = input("Enter Artist Birth Date(DD:MM:YEAR): ")

    user_input = input("Select A. Solo      B. Band: ")

    _band_id = None

    if user_input == "B":
        _band_id = browse_bands()

    if _band_id == "P":
        return

    db.session.add(
        Artist(
            name=_name,
            birth_date=_birth_date,
            band_id=_band_id
        )
    )
    db.session.commit()


def delete_artist(artist):
    db.session.delete(artist)
    db.session.commit()
    return


def shuffle_playlist(playlist):

    songs_number = playlist.songs.count()
    shuffled = list(range(0, songs_number))
    random.shuffle(shuffled)

    # playlist_songs = []
    # for song in playlist.songs:
    #     playlist_songs.append(song)
    print("Shuffled: ", shuffled)
    i = random.randint(0, songs_number-1)
    next_song = shuffled[i]
    while True:

        user_input = play_song(playlist.songs[next_song])
        if user_input == "next":
            i = (i + 1) % songs_number
            next_song = shuffled[i]
            print("i: ", i)
            continue
        elif user_input == "prev":
            i = (i - 1) % songs_number
            next_song = shuffled[i]
            continue
        elif user_input == "repeat":
            continue
        else:
            return user_input


def play_song_view(song):
    print("################################################################")
    print(song)
    print("################################################################")
    user_input = input("prev        pause        stop       repeat         next\n")
    return user_input


def time_to_sec(_time):
    formatted_time = time.strptime(_time, '%H:%M:%S')
    sleep_time = datetime.timedelta(hours=formatted_time.tm_hour,
                                    minutes=formatted_time.tm_min,
                                    seconds=formatted_time.tm_sec).total_seconds()

    return sleep_time


def play_song(song):

    player = vlc.MediaPlayer(storage_path + song.name + ".mp3")
    player.play()
    user_input = play_song_view(song)

    while True:

        if user_input == "pause":
            player.pause()
            user_input = input("prev        play        stop       repeat         next\n")

        if user_input == "play":
            player.pause()  # Calling pause again will make it continue
            user_input = input("prev        pause        stop       repeat         next\n")

        if user_input == "stop":
            player.stop()
            return user_input
        elif user_input == "next" or user_input == "prev":
            player.stop()
            return user_input
        elif user_input == "repeat":
            player.stop()
            return user_input


def footer():
    print("Q. Exit     M. Main Menu\n")


"""************************************************************************************************************
                                        Command Line Interface
************************************************************************************************************"""


main()


# play song to a certain genre

