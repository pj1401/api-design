# Songs CSV to PostgreSQL

Load datasets into PostgreSQL.

## Files

Small subsets of the datasets are included in `data-subset/` to allow faster testing.

The actual files should be placed in the `data/` directory.
The CSV files can be downloaded here: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
The HDF5 file can be downloaded here: [http://millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)

Update the path variables in the `.env` file:

```
CSV_PATH=data/Music Info.csv
CSV_LISTENING_HISTORY_PATH=data/User Listening History.csv
HDF5_PATH=data/msd_summary_file.h5
```

## Instructions

```powershell
# Copy from .example.env to .env
cp .example.env .env

# Create Secret Files
mkdir secrets
echo "admin" > secrets/admin_username.txt
echo "admin@example.com" > secrets/admin_email.txt
echo "very_secure_admin_password" > secrets/admin_password.txt

# Start container
docker-compose up

# Stop container
docker-compose down
docker-compose down -v # Removes volumes
```

Seed script imported from different repository, for full commit history see: [songs-csv-to-postgres](https://github.com/pj1401/songs-csv-to-postgres)
