import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

client_id = "150ea559aaa74f0f80373d00bf165aac"
client_secret = "08f8055e7b5e4411b98d39b4cf05c213"


client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DWWnzeQw5ZMfu?si=a8c1a600bbf14c92"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

data_dict = {"id": [], "genre": [], "track_name": [], "artist_name": [],"valence": [], "energy": []}

for track in sp.playlist_tracks(playlist_URI)["items"]:
    # URI ****
    track_uri = track["track"]["uri"]

    # Track_id ****
    track_id=track["track"]["id"]

    # Track name ****
    track_name = track["track"]["name"]

    # Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)

    # Name, popularity, genre ***
    artist_name = track["track"]["artists"][0]["name"]
    artist_genres = artist_info["genres"]

    # energy, valence ****
    track_energy=sp.audio_features(track_uri)[0]['energy']
    track_valence=sp.audio_features(track_uri)[0]['valence']

    #append in the dict
    data_dict["id"].append(track_id)
    data_dict["genre"].append(artist_genres)
    data_dict["track_name"].append(track_name)
    data_dict["artist_name"].append(artist_name)
    data_dict["valence"].append(track_valence)
    data_dict["energy"].append(track_energy)

#print(data_dict)

#Storing collected data
# Store data in dataframe
df = pd.DataFrame(data_dict)

# Drop duplicates
df.drop_duplicates(subset="id", keep="first", inplace=True)
df.to_csv("valence_arousal_dataset.csv", index=False)


