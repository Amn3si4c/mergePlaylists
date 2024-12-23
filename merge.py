from requests import HTTPError
import spotipy
import time
import os
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import argparse
import logging


# logger = logging.getLogger("examples.add_tracks_to_playlist")
# logging.basicConfig(level="DEBUG")
logging.basicConfig(
    filename=".log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logging.info("Merging Playlist")


def get_args():
    parser = argparse.ArgumentParser(description="Adds track to user playlist")
    parser.add_argument(
        "-p",
        "--playlist",
        nargs="+",
        help="List of playlists to be merged into one Merged(TIMESTAMP) playlist",
        required=True,
    )
    return parser.parse_args()


def main():
    args = get_args()
    load_dotenv("./.env")
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("REDIRECT_TO"),
            scope="playlist-read-private,playlist-modify-private",
        )
    )
    song_list = []
    for playlist in args.playlist:
        try:
            songs = sp.playlist_items(playlist)
            if songs is None:
                print("Empty Response: " + str(playlist))
                continue
            for idx, item in enumerate(songs["items"]):
                track = item["track"]
                print(
                    idx,
                    track["artists"][0]["name"],
                    " – ",
                    track["name"],
                    " - ",
                    track["uri"],
                )
                song_list.append(track["uri"])
        except HTTPError:
            print("shit")
        except SpotifyException:
            print(
                "Spotify Error \nMaybe the playlist is a playlist by spotify? (Can't be accesed)\nNon accesible URL: "
                + str(playlist)
            )
    song_list = list(set(song_list))
    currentUserId = sp.me()
    if currentUserId is None:
        print("Current User is empty")
        return
    currentUserId = currentUserId["id"]
    newPlaylist = sp.user_playlist_create(
        currentUserId, "Merged(" + str(time.time()) + ")", False, False, "Enjoy :)"
    )
    if newPlaylist is None:
        print("Couldn't create Playlist")
        return
    playlistID = newPlaylist["id"]
    sp.playlist_add_items(playlistID, song_list)


if __name__ == "__main__":
    main()
