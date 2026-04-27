"""
Loader module for seeding the database.
module: src/loader.py
"""

from typing import Any
import bcrypt
from psycopg2 import sql
import pandas as pd
from psycopg2.extensions import connection
from .user import User


def create_tables(conn: connection):
    create_tracks_table(conn)
    create_artists_table(conn)
    create_tracks_artists_table(conn)
    create_albums_table(conn)
    create_tracks_albums_table(conn)
    create_artists_albums_table(conn)
    create_users_table(conn)


def create_tracks_table(conn: connection):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id SERIAL PRIMARY KEY,
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            old_track_id VARCHAR(50)
        );
    """)
    create_table(conn, query, "tracks")


def create_artists_table(conn: connection):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS artists (
            artist_id SERIAL PRIMARY KEY,
            artist_name VARCHAR(255) CONSTRAINT temp_constraint UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            old_artist_id VARCHAR(50)
        );
    """)
    create_table(conn, query, "artists")


def create_tracks_artists_table(conn: connection):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS tracks_artists (
            track_id INTEGER,
            artist_id INTEGER,
            PRIMARY KEY (track_id, artist_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (track_id) REFERENCES tracks(track_id),
            FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
        );
    """)
    create_table(conn, query, "tracks_artists")


def create_albums_table(conn: connection):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS albums (
            album_id SERIAL PRIMARY KEY,
            album_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            old_album_id VARCHAR(50) UNIQUE
        );
    """)
    create_table(conn, query, "albums")


def create_tracks_albums_table(conn: connection):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS tracks_albums (
            track_id INTEGER,
            album_id INTEGER,
            PRIMARY KEY (track_id, album_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (track_id) REFERENCES tracks(track_id),
            FOREIGN KEY (album_id) REFERENCES albums(album_id)
        );
    """)
    create_table(conn, query, "tracks_albums")


def create_artists_albums_table(conn: connection):
    query = sql.SQL("""
        CREATE TABLE IF NOT EXISTS artists_albums (
            artist_id INTEGER,
            album_id INTEGER,
            PRIMARY KEY (artist_id, album_id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
            FOREIGN KEY (album_id) REFERENCES albums(album_id)
        );
    """)
    create_table(conn, query, "artists_albums")


def create_users_table(conn: connection):
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


def create_table(conn: connection, query: sql.SQL, table_name: str):
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()
    print(f"Created table: '{table_name}'")


def seed_database(conn: connection, data: pd.DataFrame):
    """Seed the data into the PostgreSQL database."""
    seed_artists(conn, data[["old_artist_id", "artist_name"]])
    seed_albums(conn, data[["old_album_id", "album_name"]])
    seed_tracks(
        conn,
        data[
            [
                "old_track_id",
                "name",
                "total_playcount",
                "spotify_id",
                "tags",
                "genre",
                "year",
                "duration_ms",
                "danceability",
                "mode",
                "valence",
            ]
        ],
    )

    # Seed relationships
    seed_tracks_artists(conn, data[["old_track_id", "artist_name"]])
    seed_tracks_albums(conn, data[["old_track_id", "old_album_id"]])
    seed_artists_albums(conn, data[["artist_name", "old_album_id"]])

    remove_artists_temp_constraint(conn)


def seed_admin_user(conn: connection, admin: User):
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


def seed_artists(conn: connection, artists_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in artists_data.drop_duplicates(subset=["old_artist_id"]).iterrows():
        query = """
            INSERT INTO artists (artist_name, old_artist_id)
            VALUES (%s, %s)
            ON CONFLICT (artist_name) DO UPDATE SET old_artist_id = EXCLUDED.old_artist_id;
        """
        cursor.execute(query, (row["artist_name"], row["old_artist_id"]))
    conn.commit()
    cursor.close()
    print(
        f"Seeded {len(artists_data.drop_duplicates(subset=['old_artist_id']))} artists."
    )


def seed_albums(conn: connection, albums_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in albums_data.drop_duplicates(subset=["old_album_id"]).iterrows():
        query = """
            INSERT INTO albums (album_name, old_album_id)
            VALUES (%s, %s)
            ON CONFLICT (old_album_id) DO NOTHING;
        """
        cursor.execute(
            query,
            (
                row["album_name"],
                row["old_album_id"],
            ),
        )
    conn.commit()
    cursor.close()
    print(f"Seeded {len(albums_data.drop_duplicates(subset=['old_album_id']))} albums.")


def seed_tracks(conn: connection, tracks_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in tracks_data.iterrows():
        query = """
            INSERT INTO tracks (name, total_playcount, spotify_id, tags, genre,
            year, duration_ms, danceability, mode, valence, old_track_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            query,
            (
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
                row["old_track_id"],
            ),
        )
    conn.commit()
    cursor.close()
    print(f"Seeded {len(tracks_data)} tracks.")


def seed_tracks_artists(conn: connection, tracks_artists_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in tracks_artists_data.iterrows():
        track_id = get(conn, "track_id", "tracks", "old_track_id", row["old_track_id"])
        artist_id = get(conn, "artist_id", "artists", "artist_name", row["artist_name"])
        query = """
            INSERT INTO tracks_artists (track_id, artist_id)
            VALUES (%s, %s)
            ON CONFLICT (track_id, artist_id) DO NOTHING;
        """
        cursor.execute(query, (track_id, artist_id))
    conn.commit()
    cursor.close()
    print(f"Seeded {len(tracks_artists_data)} track-artist relationships.")


def seed_tracks_albums(conn: connection, tracks_albums_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in tracks_albums_data.iterrows():
        track_id = get(conn, "track_id", "tracks", "old_track_id", row["old_track_id"])
        album_id = get(conn, "album_id", "albums", "old_album_id", row["old_album_id"])
        query = """
            INSERT INTO tracks_albums (track_id, album_id)
            VALUES (%s, %s)
            ON CONFLICT (track_id, album_id) DO NOTHING;
        """
        cursor.execute(query, (track_id, album_id))
    conn.commit()
    cursor.close()
    print(f"Seeded {len(tracks_albums_data)} track-album relationships.")


def seed_artists_albums(conn: connection, artists_albums_data: pd.DataFrame):
    cursor = conn.cursor()
    for _, row in artists_albums_data.iterrows():
        artist_id = get(conn, "artist_id", "artists", "artist_name", row["artist_name"])
        album_id = get(conn, "album_id", "albums", "old_album_id", row["old_album_id"])
        query = """
            INSERT INTO artists_albums (artist_id, album_id)
            VALUES (%s, %s)
            ON CONFLICT (artist_id, album_id) DO NOTHING;
        """
        cursor.execute(query, (artist_id, album_id))
    conn.commit()
    cursor.close()
    print(f"Seeded {len(artists_albums_data)} artist-album relationships.")


def get(
    conn: connection, fields: str, table_name: str, col_name: str, value: str
) -> tuple[Any] | None:
    """Fetch the new id by the old id.
    :param conn: The database connection.
    :param fields: A list of columns.
    :param table_name: The name of the table.
    :param col_name: The column name in the condition.
    :param value: The value in the condition.
    :returns: A tuple with one"""
    cursor = conn.cursor()
    query = sql.SQL("SELECT {select_list} FROM {table} WHERE {column} = %s").format(
        select_list=sql.Identifier(fields),
        table=sql.Identifier(table_name),
        column=sql.Identifier(col_name),
    )
    cursor.execute(query, (value,))
    conn.commit()
    fetched = cursor.fetchone()
    cursor.close()
    return fetched


def remove_artists_temp_constraint(conn: connection) -> None:
    cursor = conn.cursor()
    query = """ALTER TABLE artists DROP CONSTRAINT temp_constraint"""
    cursor.execute(query)
    conn.commit()
    cursor.close()
    print("Removed constraint unique artist_name.")
