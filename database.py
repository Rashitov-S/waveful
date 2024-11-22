import sqlite3

database = 'waveful.db'


# взаимодействие с таблицами пользователей
class UserModel:
    def __init__(self):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def add(self, login, password):
        query = 'INSERT INTO user(login, password) VALUES (?, ?)'
        self.cur.execute(query, (login, password))
        self.con.commit()

    def get(self, login):
        query = 'SELECT * FROM user WHERE login = ?'
        user = self.cur.execute(query, (login,)).fetchone()
        return user

    def get_by_id(self, user_id):
        query = 'SELECT login, password FROM user WHERE user_id = ?'
        user = self.cur.execute(query, (user_id,)).fetchone()
        return user

    def change_password(self, user_id, new_password):
        query = f"UPDATE user SET password = '{new_password}' WHERE user_id = ?"
        self.cur.execute(query, (user_id,))
        self.con.commit()


# взаимодействие с таблицей альбомов
class AlbumModel:
    def __init__(self):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def add(self, title, artist_id, path):
        if path:
            query = 'INSERT INTO album(title, artist_id, path) VALUES (?, ?, ?)'
            self.cur.execute(query, (title, artist_id, path))
        else:
            query = 'INSERT INTO album(title, artist_id) VALUES (?, ?)'
            self.cur.execute(query, (title, artist_id))
        self.con.commit()

    def get_id(self, title):
        query = 'SELECT album_id FROM album WHERE title = ?'
        album = self.cur.execute(query, (title,)).fetchone()
        return album

    def get(self, artist_id):
        query = 'SELECT album_id, title FROM album WHERE artist_id = ?'
        if not artist_id or artist_id < 0:
            query += ' OR 1=1'
        albums = self.cur.execute(query, (artist_id,)).fetchall()
        return albums

    def get_image(self, album_id):
        query = 'SELECT path FROM album WHERE album_id = ?'
        path = self.cur.execute(query, (album_id,)).fetchone()
        return path

    def get_title(self, album_id):
        query = 'SELECT title FROM album WHERE album_id = ?'
        album = self.cur.execute(query, (album_id,)).fetchone()
        return album


# взаимодействие с таблицей артистов
class ArtistModel:
    def __init__(self):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def add(self, name):
        query = 'INSERT INTO artist(name) VALUES (?)'
        self.cur.execute(query, (name,))
        self.con.commit()

    def get(self, name, artist_id=None):
        query = f"SELECT artist_id, name FROM artist WHERE name LIKE '%{name}%' OR artist_id = '{artist_id}'"
        if not name:
            query += ' OR 1=1'
        artists = self.cur.execute(query).fetchall()
        return artists

    def get_name(self, artist_id):
        query = 'SELECT name FROM artist WHERE artist_id = ?'
        artist = self.cur.execute(query, (artist_id,)).fetchone()
        return artist


# взаимодействие с таблицей треков
class TrackModel:
    def __init__(self):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def add(self, title, artist_id, album_id, path):
        query = 'INSERT INTO tracks(title, artist_id, album_id, path) VALUES (?, ?, ?, ?)'
        self.cur.execute(query, (title, artist_id, album_id, path))
        self.con.commit()

    def get(self, track_id=None, title=None):
        query = f"SELECT * FROM tracks WHERE track_id = '{track_id}' OR title = '{title}'"
        if not track_id:
            query += ' OR 1=1'
        tracks = self.cur.execute(query).fetchall()
        return tracks

    def search(self, title):
        query = f"SELECT * FROM tracks WHERE title LIKE '%{title}%'"
        tracks = self.cur.execute(query).fetchall()
        return tracks

    def get_max_id(self):
        query = f"SELECT MAX(track_id) FROM tracks"
        id = self.cur.execute(query).fetchone()
        return id


class FavouriteModel:
    def __init__(self):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def add(self, user_id, track_id):
        query = 'INSERT INTO favourite_tracks(user_id, track_id) VALUES (?, ?)'
        self.cur.execute(query, (user_id, track_id))
        self.con.commit()

    def delete(self, user_id, track_id):
        query = 'DELETE FROM favourite_tracks WHERE user_id = ? AND track_id = ?'
        self.cur.execute(query, (user_id, track_id))
        self.con.commit()

    def get_tracks(self, user_id):
        query = f"SELECT track_id FROM favourite_tracks WHERE user_id = ?"
        tracks = self.cur.execute(query, (user_id,)).fetchall()
        return tracks

    def get_track(self, user_id, track_id):
        query = f"SELECT user_id, track_id FROM favourite_tracks WHERE user_id = ? AND track_id = ?"
        track = self.cur.execute(query, (user_id, track_id)).fetchone()
        print(user_id, track_id)
        return track
