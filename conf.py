from musicly import *


def migrate():
    db.create_all()

    changes = []

    changes.append(Playlist(title='playlist1', description='desc'))
    changes.append(Playlist(title='playlist2', description='desc'))

    changes.append(Band(name='David Guetta'))
    changes.append(Band(name='Backstreet Boys'))

    changes.append(Artist(name='Sia', birth_date='02-07-1990'))
    changes.append(Artist(name='Bruno Mars', birth_date='02-07-1990'))
    changes.append(Artist(name='David Guetta Member 1', birth_date='02-07-1990', band_id=1))
    changes.append(Artist(name='David Guetta Member 2', birth_date='02-07-1990', band_id=1))
    changes.append(Artist(name='Backstreet Boys Member 1', birth_date='02-07-1990', band_id=2))
    changes.append(Artist(name='Backstreet Boys Member 2', birth_date='02-07-1990', band_id=2))

    changes.append(Album(title='album1', artist_id=1))
    changes.append(Album(title='album2', band_id=1))

    changes.append(Song(name='Song1',
                        album_release_date='2019',
                        genres='Pop',
                        lyrics='lyrics',
                        length='00:03:14',
                        band_id=1,
                        album_id=2))
    changes.append(Song(name='Song2',
                        album_release_date='2017',
                        genres='Rock',
                        lyrics='lyrics',
                        length='00:05:04',
                        artist_id=1,
                        album_id=1))

    add_all(db, changes)
    db.session.commit()


def rollback(database):
    database.drop_all()


def add_song():
    _name = input("Enter Name: ")
    _genres = input("Enter Genre: ")
    _album_release_date = "2019"
    _lyrics = "Lyrics"
    _length = '00:03:14'

    user_input = input("Enter S. Single or A. Album: ")

    _album = None
    if user_input == "A":
        _album = browse_albums()

    user_input = input("Enter A. Artist or B. Band      C. Both: ")

    _band_id = None
    _artist_id = None

    if user_input == "A":
        _artist_id = _album.artist.id
    elif user_input == "B":
        _band_id = _album.band.id
    elif user_input == "C":
        _band_id = _album.band.id
        _artist_id = _album.artist.id

    if _band_id == "P" or _artist_id == "P" or _album == "P":
        return

    db.session.add(
        Song(
            name=_name,
            album_release_date=_album_release_date,
            genres=_genres,
            lyrics=_lyrics,
            length=_length,
            band_id=_band_id,
            album_id=_album.id,
            artist_id=_artist_id
        )
    )
    db.session.commit()


def add_artist(database, artist):
    add_all(database, [artist])
    db.session.commit()


def add_band(database, band):
    add_all(database, [band])
    db.session.commit()


def add_all(database, changes):
    for element in changes:
        database.session.add(element)


artists = [
    Artist(name='Alan Walker', birth_date='02:12:1990'),
    Artist(name='Clean Bandit', birth_date='02:12:1990'),
    Artist(name='Bazzi', birth_date='02:12:1990'),
    Artist(name='Flo Rida', birth_date='02:12:1990'),
    Artist(name='Wiz Khalifa', birth_date='02:12:1990'),
    Artist(name='Charlie Puth', birth_date='02:12:1990')
]


alan_walker = Artist.query.filter_by(name='Alan Walker').first()
bazzi = Artist.query.filter_by(name='Bazzi').first()
clean_bandit = Artist.query.filter_by(name='Clean Bandit').first()
flo_rida = Artist.query.filter_by(name='Flo Rida').first()
wiz_khalifa = Artist.query.filter_by(name='Wiz Khalifa').first()

imagine_dragons = Band.query.filter_by(name='Imagine Dragons').first()
one_direction = Band.query.filter_by(name='One Direction').first()
chainsmokers = Band.query.filter_by(name='The Chainsmokers').first()


bands = [
    Band(name='David Guetta'),
    Band(name='Imagine Dragons'),
    Band(name='One Direction'),
    Band(name='The Chainsmokers'),
    Band(name='Backstreet Boys'),
]

songs = [
    Song(name='Alan_Walker_Faded', artist_id=alan_walker.id, album_release_date='2019', genres='Pop', lyrics='lyrics', length='00:03:14'),
    Song(name='Bazzi_Beautiful', artist_id=bazzi.id, album_release_date='2019', genres='Pop', lyrics='lyrics', length='00:03:14'),
    Song(name='Clean_Bandit_Rockabye', artist_id=clean_bandit.id, album_release_date='2019', genres='Rock', lyrics='lyrics', length='00:03:14'),
    Song(name='Flo_Rida_Whistle', artist_id=flo_rida.id, album_release_date='2019', genres='Pop', lyrics='lyrics', length='00:03:14'),
    Song(name='Imagine_Dragons_Believer', band_id=imagine_dragons.id, album_release_date='2019', genres='Pop', lyrics='lyrics', length='00:03:14'),
    Song(name='Imagine_Dragons_Whatever_It_Takes', band_id=imagine_dragons.id, album_release_date='2019', genres='Pop', lyrics='lyrics', length='00:03:14'),
    Song(name='One_Direction_Perfect', band_id=one_direction.id, album_release_date='2019', genres='Pop', lyrics='lyrics', length='00:03:14'),
    Song(name='The_Chainsmokers_Dont_Let_Me_Down', band_id=chainsmokers.id, album_release_date='2019', genres='Rock', lyrics='lyrics', length='00:03:14'),
    Song(name='Wiz_Khalifa_See_You_Again_ft_Charlie_Puth', artist_id=wiz_khalifa.id, album_release_date='2019', genres='Pop', lyrics='lyrics', length='00:03:14')
]
