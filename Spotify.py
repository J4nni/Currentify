import spotipy
import spotipy.util as util
import json
import requests

req=requests

token = util.prompt_for_user_token(
        username='$your username',
        scope='user-read-private user-read-currently-playing user-library-modify playlist-read-collaborative playlist-modify-public playlist-modify-private',
        client_id='XXX', #Add your Client ID
        client_secret='XXX', #Add your Client Secret
        redirect_uri='http://google.com/')

spotify = spotipy.Spotify(auth=token)
hed = {'Authorization': 'Bearer ' + token}
insa = req.get(url="https://api.spotify.com/v1/me/player/currently-playing", headers=hed) #Get your Current Song
play=req.get(url="https://api.spotify.com/v1/me/playlists", headers=hed) #Get your Playlists


rawjson= json.loads(insa.content) #Check the Currentsong 
if rawjson['is_playing'] is False:
    exit(print("Hey you don't listen any Music in Spotify?!"))
else:
    itemkey= rawjson ['item']
    TrackUrl=itemkey['id']
    ActuallySong=[TrackUrl] #The Endpoint needs a List to add the Song 
    playlistjs=play.content
    playlists= json.loads(playlistjs)
    items=playlists['items']
    increment=0
    Titel=[]
    playid=[]
    for playlist in items: #Here we catch the information of the Playlists.
        s= items[increment]
        d=s['id']
        n=s['name']
        collab=s['collaborative']
        owners=s['owner']
        displayname=owners['display_name']
        if collab is False and displayname != '$yourusername' : #catch Protected Playlist
            newbuild= str(increment) +" "+ n
            Titel+=[newbuild]
            playid+=[d]
            print (str(increment)+" "+"no Permission for Playlist "+n +" to add songs")
            increment = increment+1
        else: #here we build the informations
            newbuild= str(increment) +" "+ n 
            Titel+=[newbuild]
            playid+=[d]
            print (Titel[increment])
            increment = increment+1
            f=True
while f is True:
    try: #here comes the input
        ins=input("Take a number: ")
        nummer=int(ins)
        f= False
    except ValueError:
        print("Only Integers !")
        f= True

try:
   spotify.user_playlist_add_tracks('$username',playid[nummer],ActuallySong)
except spotipy.client.SpotifyException as identifier:
 print("No Permission")
