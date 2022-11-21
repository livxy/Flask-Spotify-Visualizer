import os
import sys
import decimal
import dotenv
import spotipy
import spotipy.util as util
from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
import numpy as np
import colorsys
import requests
import scipy
import binascii
app = Flask(__name__)

# Load the environment variables
dotenv.load_dotenv()

# Spotify API credentials
client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
username = os.getenv('SPOTIFY_USERNAME')
scope = 'user-read-currently-playing'

# Get the user's access token
if token := util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri='http://localhost:8080/'):
    sp = spotipy.Spotify(auth=token)

# Get the current song playing on the user's Spotify account
def get_current_song():
    return sp.current_user_playing_track()

# Get the song's name, artist, and album art
def get_song_info(current_song):
    song_name = current_song['item']['name']
    song_artist = current_song['item']['artists'][0]['name']
    song_album_art = current_song['item']['album']['images'][0]['url']
    return song_name, song_artist, song_album_art

# Get the song's audio features
def get_song_features(current_song):
    song_id = current_song['item']['id']
    return sp.audio_features(song_id)

# Display the song's name, artist, and album art on Flask
@app.route('/')
def index(): 
    current_song = get_current_song()
    song_features = get_song_features(current_song)
    current_song = get_current_song()
    song_name, song_artist, song_album_art = get_song_info(current_song)
    print(get_song_features(current_song))
    print(get_song_info(current_song))

    #? get_song_features(current_song) returns a list of dictionaries -
    #? danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness,
    #? valence, tempo, type, id, uri, track_href, analysis_url, duration_ms, time_signature
    # [{'danceability': 0.658, 'energy': 0.683, 'key': 9, 'loudness': -8.219, 'mode': 1, 'speechiness': 0.319, 'acousticness': 0.0651, 'instrumentalness': 0, 'liveness': 0.2, 'valence': 0.178, 'tempo': 144.001, 'type': 'audio_features', 'id': '6x3BWyMi95035qz5pB8snv', 'uri': 'spotify:track:6x3BWyMi95035qz5pB8snv', 'track_href': 'https://api.spotify.com/v1/tracks/6x3BWyMi95035qz5pB8snv', 'analysis_url': 'https://api.spotify.com/v1/audio-analysis/6x3BWyMi95035qz5pB8snv', 'duration_ms': 192115, 'time_signature': 4}]

    #? get_song_info(current_song) returns a tuple - (song_name, song_artist, song_album_art)
    # ('off the leash! (feat. yvngxchris and Luisss)', 'tana', 'https://i.scdn.co/image/ab67616d0000b273c44c0b18f15140d3d9e4ef51')

    duration = song_features[0]["duration_ms"]

    artist = sp.search(q=f'artist:{song_artist}', type='artist')
    artist_image = artist['artists']['items'][0]['images'][0]['url']
    # print(artist_image)


    def get_average_color(art):
        im = Image.open(requests.get(art, stream=True).raw)
        im = im.resize((150, 150))      # optional, to reduce time
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

        n_colors = 1
        codes, dist = scipy.cluster.vq.kmeans(ar, n_colors)
        vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
        counts, bins = np.histogram(vecs, len(codes))    # count occurrences

        index_max = np.argmax(counts)                    # find most frequent
        peak = codes[index_max]
        finalcolor = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
        return finalcolor
    
    #! Fix this dogshit code
    #! lol just kidding i dont know how to make a goddamn template :sob: 
    return f"""
  <script>
    setTimeout(function(){{
        location.reload();
    }}, {duration_ms / 1000});    
  </script>
  <style>
    * {{
      box-sizing: border-box; 
      background-color: #121212;
    }}
    body {{
      margin: 40px;
      padding-bottom: 100px;
    }}
    h1 {{
      text-align: center;
      font-size: 2.5rem;
      font-family: Roboto;
      margin-top: 50px;
      color: #1db954;
    }}
    p {{
      color: #b3b3b3;
      font-size: 1.5rem;
      font-family: Roboto;
      text-align: center;
    }}
    img {{
      display: block;
      margin-left: auto;
      margin-right: auto;
    }}
    .artist {{
      border-radius: 50%;
      box-shadow: 0 0 20px 5px #{get_average_color(artist_image)};
    }}
    .album {{
      box-shadow: 0 0 20px 5px #{get_average_color(song_album_art)};
    }}
    .tab-out {{
      display: flex;
      align-items: flex-end;
      margin-right: 50px;
      
    }}
  </style>

  <body>
    <h1>Song Name</h1>
    <p>{song_name}</p>
    <h1>Artist</h1>
    <p>{song_artist}</p>
    <img
      class="artist"
      src="{artist_image}"
      alt="Artist Image"
      style="width: 200px; height: 200px"
    />
    <h1>Album Art</h1>
    <img
      class="album"
      src="{song_album_art}"
      alt="Album Art"
      width="300"
      height="300"
    />

    <h1>Audio Features</h1>
    <div class="tab-out">
      <p>Danceability: {song_features[0]["danceability"]}</p>
      <p>Energy: {song_features[0]["energy"]}</p>
      <p>Key: {song_features[0]["key"]}</p>
      <p>Loudness: {song_features[0]["loudness"]}</p>
      <p>Mode: {song_features[0]["mode"]}</p>
      <p>Speechiness: {song_features[0]["speechiness"]}</p>
      <p>Acousticness: {song_features[0]["acousticness"]}</p>
      <p>Instrumentalness: {song_features[0]["instrumentalness"]}</p>
      <p>Liveness: {song_features[0]["liveness"]}</p>
      <p>Valence: {song_features[0]["valence"]}</p>
      <p>Tempo: {song_features[0]["tempo"]} bpm</p>
      <p>Duration: {duration // 60000}:{(duration % 60000) // 1000:02}</p>
      <p>Time Signature: {song_features[0]["time_signature"]}</p>
    </div>
  </body>

            """
    # current_song = get_current_song()
    # song_name, song_artist, song_album_art = get_song_info(current_song)
    # return f'<h1>{song_name}</h1> <h2>{song_artist}</h2> <img src="{song_album_art}" alt="Album Art" width="300" height="300">'

# Display the song's audio features on Flask 
# @app.route('/features')
# def features():

# Display the song's audio analysis on Flask
# @app.route('/analysis')
# def analysis():
#     current_song = get_current_song()
#     song_analysis = get_song_analysis(current_song)
#     return render_template('analysis.html', song_analysis=song_analysis)

if __name__ == '__main__':
    app.run(debug=True)

