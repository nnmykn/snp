# -*- coding: utf-8 -*-
import spotipy
import tweepy
import urllib.request
import urllib
import time

#SpotifyとTwitterへのAPI認証
client_id = 'クライアントID'
client_secret = 'クライアントシークレットID'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

CK = "ここにConsumer Key"
CS = "ここにConsumer Secret"
AT = "ここにAccess Token"
ATS = "ここにAccess Token Secret"
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth)
#認証おわり

music_title = ""
msc = " "

while True:
    try:
        token = spotipy.util.prompt_for_user_token(
            username="ユーザーネーム",
            scope="user-read-currently-playing",
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="https://example.com/callback/"
        )

        spotify = spotipy.Spotify(auth=token)
        current_playing = spotify.current_user_playing_track()

        music_title = current_playing['item']['name']
        artist_name = current_playing['item']['artists'][0]['name']

        music_title = music_title.replace(' ', '')  # スペースがあると画像生成でエラー出るのでなくす。全角半角どっちとも。
        music_title = music_title.replace('　', '')
        artist_name = artist_name.replace(' ', '')
        artist_name = artist_name.replace('　', '')
        if music_title == msc:
            print("曲同じやんけ！")
            time.sleep(30)
        else:
            msc = music_title

            img_url = 'https://res.cloudinary.com/nixo/image/upload/l_text:Sawarabi%20Gothic_120_bold:' + urllib.parse.quote_plus(music_title, encoding='utf-8') + "-" + urllib.parse.quote_plus(artist_name, encoding='utf-8') + ',co_rgb:333,w_1300,c_fit/v1609768419/nowplay_kzuxtk.png'
            img_url = img_url.replace(' ', '') #スペースがあると画像生成でエラー出るのでなくす
            img_url = img_url.replace('　', '')
            img_save_name = "music.png"
            urllib.request.urlretrieve(str(img_url), img_save_name)

            try:
                api.update_with_media(filename = "./music.png", status = f"SongTitle: {music_title}\nArtist: {artist_name}\n \n#NowPlaying")
                print("ツイートしました")
            except Exception as e:
                print("ツイートに失敗しました")
                print(e)

            time.sleep(120)
    except Exception as e:
        print("エラーが発生しました")
        print(e)
        time.sleep(60)
