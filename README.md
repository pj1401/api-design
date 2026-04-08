# API Design Assignment

## Tracks REST API

**Primary resource:** Tracks (track_id, track_name, duration_ms, genre, year, tags, total_playcount, danceability, mode, valence)

**Secondary resource 1:** Artists (artist_id, artist_name, albums)

**Secondary resource 2:** Albums (album_id, album_name, total_tracks, album_type, release_date, artists, tracks)

Dataset: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
För albumnamn, album_id, och artist_id: [http://millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)

## Seed database

### Files

Small subsets of the datasets are included in `seed/data-subset/` to allow faster testing.

The actual files should be placed in the `seed/data/` directory.  
The CSV files can be downloaded here: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
The HDF5 file can be downloaded here: [http://millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)

Update the path variables in the `.env` file:

```
CSV_PATH=data/Music Info.csv
CSV_LISTENING_HISTORY_PATH=data/User Listening History.csv
HDF5_PATH=data/msd_summary_file.h5
```

Update `seed/Dockerfile`, so the correct dataset files are copied.

```dockerfile
# Copy the src directory and seed.py
COPY seed/src ./src
COPY seed/seed.py .
# COPY seed/data-subset/ ./data-subset
COPY seed/data/ ./data
```

### Instructions

```powershell
# Copy from .example.env to .env
cp .example.env .env

# Create Secret Files
mkdir secrets
echo "admin" > secrets/admin_username.txt
echo "admin@example.com" > secrets/admin_email.txt
echo "very_secure_admin_password" > secrets/admin_password.txt

# Start container for db and seed script
docker-compose up db seed
docker-compose up db      # Start only database

# Stop container
docker-compose down
docker-compose down -v # Removes volumes
```

## Run dev

### Setup env

The app uses ECDSA for JWT signing.  
To generate the key pair:

```bash
# Generate private key
openssl ecparam -name secp521r1 -genkey -noout -out tracks-rest-api-jwt.pem

# Extract public key
openssl ec -in tracks-rest-api-jwt.pem -pubout -out tracks-rest-api-jwt.public.pem
```

Copy the contents of the key pair files to the `.env` file.

### Run

```powershell
# Change to the api directory
cd api/

# Start the database
docker-compose up db -d

# Run the app
uv run -- flask --app main run --debug

# Stop the database
docker-compose down
```
