from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
USER_ID = os.environ.get("USER_ID")
SP_ENDPOINT = f"https://api.spotify.com/v1/users/{USER_ID}/playlists"


date = input("Which year do you want to teleport to? Type the date in this format YYYY-MM-DD: ")
URL = f"https://www.billboard.com/charts/hot-100/2000-08-12/"

response = requests.get(url=URL)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")
song_titles = soup.select("li ul li h3")
song_list = [song.getText().strip() for song in song_titles]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-private",
        cache_path="token.txt",
        username=USER_ID,
        show_dialog=True
    )
)

user_id = sp.current_user()["id"]
year = date.split("-")[0]

song_uri = []

for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    description="top 100 music from date in past."
)

sp.playlist_add_items(
    playlist_id=playlist["id"],
    items=song_uri
)
