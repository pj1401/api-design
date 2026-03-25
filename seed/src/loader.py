"""
Loader module for seeding the database.
"""

import bcrypt
from psycopg2 import sql
import pandas as pd

from .user import User


def create_tables(conn):
    create_tracks_table(conn)
    create_artists_table(conn)
    create_tracks_artists_table(conn)
    create_albums_table(conn)
    create_tracks_albums_table(conn)
    create_artists_albums_table(conn)
    create_users_table(conn)


def create_tracks_table(conn):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(255),
            total_playcount BIGINT DEFAULT 0,
            spotify_id VARCHAR(255),
            tags VARCHAR(255),
            genre VARCHAR(255),
            year INT,
            duration_ms INT,
            danceability FLOAT,
            mode INT,
            valence FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    create_table(conn, query, "tracks")


def create_artists_table(conn):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS artists (
            artist_id VARCHAR(50) PRIMARY KEY,
            artist_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    create_table(conn, query, "artists")


def create_tracks_artists_table(conn):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS tracks_artists (
            track_id VARCHAR(50),
            artist_id VARCHAR(50),
            PRIMARY KEY (track_id, artist_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (track_id) REFERENCES tracks(track_id),
            FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
        );
    """)
    create_table(conn, query, "tracks_artists")


def create_albums_table(conn):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS albums (
            album_id VARCHAR(50) PRIMARY KEY,
            album_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    create_table(conn, query, "albums")


def create_tracks_albums_table(conn):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS tracks_albums (
            track_id VARCHAR(50),
            album_id VARCHAR(50),
            PRIMARY KEY (track_id, album_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (track_id) REFERENCES tracks(track_id),
            FOREIGN KEY (album_id) REFERENCES albums(album_id)
        );
    """)
    create_table(conn, query, "tracks_albums")


def create_artists_albums_table(conn):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS artists_albums (
            artist_id VARCHAR(50),
            album_id VARCHAR(50),
            PRIMARY KEY (artist_id, album_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
            FOREIGN KEY (album_id) REFERENCES albums(album_id)
        );
    """)
    create_table(conn, query, "artists_albums")


def create_users_table(conn):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            permission_level INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    create_table(conn, query, "albums")


def create_table(conn, query: sql.SQL, table_name: str):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    print(f"Created table: '{table_name}'")


def seed_database(conn, data: pd.DataFrame):
    """Seed the data into the PostgreSQL database."""
    seed_artists(conn, data[["artist_id", "artist_name"]])
    seed_albums(conn, data[["album_id", "album_name"]])
    seed_tracks(conn, data[["track_id", "name", "total_playcount", "spotify_id", "tags", "genre", "year", "duration_ms", "danceability", "mode", "valence"]])

    # Seed relationships
    seed_tracks_artists(conn, data[["track_id", "artist_id"]])
    seed_tracks_albums(conn, data[["track_id", "album_id"]])
    seed_artists_albums(conn, data[["artist_id", "album_id"]])


def seed_admin_user(conn, admin: User):
    cursor = conn.cursor()
    query = """
        INSERT INTO users (username, email, password_hash, permission_level)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (username) DO NOTHING;
    """
    admin_password_hash = bcrypt.hashpw(
        admin.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    cursor.execute(query, (admin.username, admin.email, admin_password_hash, 1))
    conn.commit()
    cursor.close()
    print("Seeded admin user.")


def seed_artists(conn, artists_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in artists_data.drop_duplicates(subset=["artist_id"]).iterrows():
        query = """
            INSERT INTO artists (artist_id, artist_name)
            VALUES (%s, %s)
            ON CONFLICT (artist_id) DO NOTHING;
        """
        cursor.execute(query, (row["artist_id"], row["artist_name"]))
    conn.commit()
    cursor.close()
    print(f"Seeded {len(artists_data.drop_duplicates(subset=['artist_id']))} artists.")


def seed_albums(conn, albums_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in albums_data.drop_duplicates(subset=["album_id"]).iterrows():
        query = """
            INSERT INTO albums (album_id, album_name)
            VALUES (%s, %s)
            ON CONFLICT (album_id) DO NOTHING;
        """
        cursor.execute(query, (row["album_id"], row["album_name"]))
    conn.commit()
    cursor.close()
    print(f"Seeded {len(albums_data.drop_duplicates(subset=['album_id']))} albums.")


def seed_tracks(conn, tracks_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in tracks_data.iterrows():
        query = """
            INSERT INTO tracks (track_id, name, total_playcount, spotify_id, tags, genre,
            year, duration_ms, danceability, mode, valence)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (track_id) DO NOTHING;
        """
        cursor.execute(
            query,
            (
                row["track_id"],
                row["name"],
                int(row["total_playcount"]),
                row["spotify_id"],
                row["tags"],
                row["genre"],
                row["year"],
                row["duration_ms"],
                row["danceability"],
                row["mode"],
                row["valence"],
            ),
        )
    conn.commit()
    cursor.close()
    print(f"Seeded {len(tracks_data)} tracks.")


def seed_tracks_artists(conn, tracks_artists_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in tracks_artists_data.iterrows():
        query = """
            INSERT INTO tracks_artists (track_id, artist_id)
            VALUES (%s, %s)
            ON CONFLICT (track_id, artist_id) DO NOTHING;
        """
        cursor.execute(query, (row["track_id"], row["artist_id"]))
    conn.commit()
    cursor.close()
    print(f"Seeded {len(tracks_artists_data)} track-artist relationships.")


def seed_tracks_albums(conn, tracks_albums_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in tracks_albums_data.iterrows():
        query = """
            INSERT INTO tracks_albums (track_id, album_id)
            VALUES (%s, %s)
            ON CONFLICT (track_id, album_id) DO NOTHING;
        """
        cursor.execute(query, (row["track_id"], row["album_id"]))
    conn.commit()
    cursor.close()
    print(f"Seeded {len(tracks_albums_data)} track-album relationships.")


def seed_artists_albums(conn, artists_albums_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in artists_albums_data.iterrows():
        query = """
            INSERT INTO artists_albums (artist_id, album_id)
            VALUES (%s, %s)
            ON CONFLICT (artist_id, album_id) DO NOTHING;
        """
        cursor.execute(query, (row["artist_id"], row["album_id"]))
    conn.commit()
    cursor.close()
    print(f"Seeded {len(artists_albums_data)} artist-album relationships.")
