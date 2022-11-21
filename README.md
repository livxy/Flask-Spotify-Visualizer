# Spotify-Visualizer
W.I.P. project using flask and python to display Spotify, but in a simplistic manner.

![image](https://user-images.githubusercontent.com/67598470/202959948-b937d9fa-254d-4df4-abd8-1ff912bf77af.png)

N.T.S. - ![image](https://user-images.githubusercontent.com/67598470/202955987-91c1a1c5-2b52-4bd1-8a33-c6f5abe5a79c.png)


## EASY TO USE:
1. Make a file called ".env"
2. Input the file with the following:
```env
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIFY_USERNAME = ""
```
You can find your Spotify Client ID & Client Secret by making an application at https://developer.spotify.com/

3. Go to your Spotify application and click Edit Settings

![image](https://user-images.githubusercontent.com/67598470/202961276-cfb2ec96-db78-4725-8b6d-72a8a693b552.png)

4. Add `http://localhost:8080/` as your Redirect URL
5. Install the requirements by running `pip install -r requirements.txt`
6. Run the file called `main.py`
7. It should open your browser and ask for authorization. Click ok on that. If you didn't get redirected to `http://localhost:8080/`, type that link in your browser. It should work, just play a song/restart it and refresh the site to get it to automatically refresh :) 
