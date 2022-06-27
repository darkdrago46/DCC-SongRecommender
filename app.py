from email.mime import application
import pandas as pd
import numpy as np
from numpy.linalg import norm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from flask import Flask,request, url_for, redirect, render_template 



#function to remove digits from a list
def remove(list):
    pattern = '[0-9]'
    list = [re.sub(pattern, '', i) for i in list]
    return list

#authorize
client_id = "150ea559aaa74f0f80373d00bf165aac"
client_secret = "08f8055e7b5e4411b98d39b4cf05c213"

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


df = pd.read_csv("songDataset.csv")

df["mood_vec"] = df[["valence", "energy"]].values.tolist()

#opening the input - "https://open.spotify.com/playlist/37i9dQZF1DWWnzeQw5ZMfu?si=a8c1a600bbf14c92"
#playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbfE9uIs0prNn?si=060ae1547b154028"
#playlist_link=input('ENTER SPOTIFY PLAYLIST LINK HERE:')


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("spotify.html")


@app.route('/predict',methods=['POST'])
def predict():
    playlist_link=request.form.get('urlName')
    playlist_URI = str(playlist_link).split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        # URI ****
        track_uri = track["track"]["uri"]

        # Track_id ****
        track_id=track["track"]["id"]

        # Track name ****
        #track_name = track["track"]["name"]

        # Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)

        # Name, popularity, genre ***
        artist_name = track["track"]["artists"][0]["name"]
        artist_genres = artist_info["genres"]

        # energy, valence ****
        track_energy=sp.audio_features(track_uri)[0]['energy']
        track_valence=sp.audio_features(track_uri)[0]['valence']


    n_recs = 5
    ref_df=df
    track_moodvec=np.array([track_valence, track_energy])
    ref_df["distances"] = ref_df["mood_vec"].apply(lambda x: norm(track_moodvec - np.array(x)))
    ref_df_sorted = ref_df.sort_values(by="distances", ascending=True)
    ref_df_sorted = ref_df_sorted[ref_df_sorted["id"] != track_id]

    #print(ref_df_sorted.iloc[:n_recs])

    recomm_df=pd.DataFrame(ref_df_sorted.iloc[:n_recs])
    #print(recomm_df.info())
    recomm_songs_object=recomm_df['track_name']
    recomm_songs_list=recomm_songs_object.to_list()
    return render_template('spotify.html',pred=recomm_songs_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)




