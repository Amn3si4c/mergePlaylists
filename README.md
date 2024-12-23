# mergePlaylists
Small python script to merge Spotify playlist
## Usage
```
python3 merge.py -p [spotifyPlaylistURL] [spotifyPlaylistURL] ....
```
## .env file
Needs .env file which looks like this:
```
CLIENT_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLIENT_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
REDIRECT_TO="http://localhost:8080/callback"
```
`CLIENT_SECRET` `CLIENT_ID` and `REDIRECT_TO` need to be set/retrieved via the spotify developer portal
