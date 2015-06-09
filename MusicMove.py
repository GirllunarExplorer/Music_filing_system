__author__ = 'GirlLunarExplorer'

import argparse
from string import capwords
import discogs_client as discogs
import os
import shutil
import string

consumer_key = 'rAjSgwbCPsRVZbJoyvmt'
consumer_secret = 'fNTLMBiFlLerIgIuyKIytckvOrqqcOpv'
request_token_url = 'http://api.discogs.com/oauth/request_token'
authorize_url = 'http://www.discogs.com/oauth/authorize'
access_token_url = 'http://api.discogs.com/oauth/access_token'

discogs.user_agent = 'MyMusicPythonProject'

def set_destination():
    default = '/Users/tracyrohlin/Music/iTunes/iTunes Media/Music'
    itunes_path = raw_input("Please enter destination path.  Default is {0} \n".format(default))
    if not itunes_path:
        itunes_path = default
    return itunes_path

def check_file_tag(song):
    if song.endswith(".m4a"):
        return ".m4a"
    elif song.endswith(".mp3"):
        return ".mp3"
    elif song.endswith(".m4p"):
        return ".m4p"
    else:
        return ".flac"

def check_unwanted_chars(song):
    import re

    # gets rid of (featuring artist) and (ft. artist) from file name

    feat_pattern = re.compile(r'.feat.+')
    ft_pattern = re.compile(r'(ft.+)')
    patterns = [feat_pattern, ft_pattern]
    for pattern in patterns:
        match = re.search(pattern, song)
        if match:
            song = pattern.sub("", song)[:-1]


    # forces capitalization after a parentheses
    pattern = re.compile(r"\(")
    p_match = re.finditer(pattern, song)
    if p_match:
        i = 0
        for item in p_match:
            i = item.start()+1
        song = song[:i]+ song[i:].capitalize()
    return song


class Music_paths(object):
    def __init__(self, album_path, album_name, album_type, artist_name):
        super(Music_paths,self).__init__()
        self.album_path = album_path
        self.album_name = album_name
        self.album_type = album_type
        self.artist_name = artist_name

        self.itunes_path = set_destination()
        self.target_album = None


        self.client = discogs.Client('test client') #discogs limits tokens to 100 a day so keys cannot be kept as permanent variables
        self.client.set_consumer_key(consumer_key, consumer_secret)
        print "follow this url to authorize the client"
        print self.client.get_authorize_url()[2]
        new_key = raw_input()
        self.client.get_access_token(new_key)


    def get_target_album(self):
        # Goes through all of the releases that match that album,
        # prints each track and asks if it is the correct album.
        # This is done because discogs allows users to upload different versions of the same release
        # so it is possible to have several different versions of the same album in the database
        # with slight variations in tracks and so on.

        releases = [x for x in self.client.search(self.album_name, artist = self.artist_name)]
        while releases and not self.target_album:
            releases.reverse() # I've noticed the most accurate matches tend to be at the end of the release list
            current = releases.pop()
            for track in current.tracklist:
                print track
            answer = raw_input("does this look correct?\n")
            if answer.lower() =="yes":
                self.target_album = current
            else: pass
        print "going to use", self.target_album
        return self.target_album

    def standard_album(self):
        self.target_album = self.get_target_album()

        possible_paths =[self.artist_name, self.album_name]
        for path in possible_paths:
            #creates a separate folder for the artist and then the album if it does not exist
            if not os.path.exists(self.itunes_path+path):
                os.mkdir(self.itunes_path+path)
            self.itunes_path += path +"/"

        for track in self.target_album.tracklist:

            for song in os.listdir(self.album_path):
                if track.title.lower() in song.lower():
                    file_tag = check_file_tag(song)
                    title = check_unwanted_chars(capwords(track.title))
                    source = "{0}/{1}".format(self.album_path, song)
                    dest = "{0}{1}{2}".format(self.itunes_path,title,file_tag)
                    shutil.copyfile(source, dest)
                    print "Moving to {0}".format(dest)

    def non_standard_album(self,):
        self.target_album = self.get_target_album()
        self.album_type = string.capwords(self.album_type)+"s"

        # creates a separate compilations/soundtrack/singles folder
        possible_paths =[self.album_type, self.album_name]
        for path in possible_paths:
            if not os.path.exists(self.itunes_path+path):
                os.mkdir(self.itunes_path+path)
            self.itunes_path += path +"/"

        #asks for artists names for songs in order to make a "artistname - songname.mp3" format
        for track in self.target_album.tracklist:
            compilation_artist = raw_input("who is the artist for {}\n".format(track.title))
            for song in os.listdir(self.album_path):
                if track.title.lower() in song.lower():
                    file_tag = check_file_tag(song)
                    title = check_unwanted_chars(capwords(track.title))
                    source = "{0}/{1}".format(self.album_path, song)
                    dest = "{0}{1} - {2}{3}".format(self.itunes_path,compilation_artist,title,file_tag)
                    try:
                        shutil.copyfile(source,  dest)
                        print "Moving to {0}".format(dest)
                        break
                    except Exception as error:
                        print error
                        print "Will not accept foreign characters, including characters with accent marks on them"




def main(album_path, album_name, album_type, artist_name):

    album = Music_paths(album_path, album_name, album_type, artist_name)
    known_types = ["standard", "soundtrack", "compilation", "single"]

    if album.album_type.lower() == "standard":
        album.standard_album()
    elif album.album_type.lower() not in known_types:
        print album_type + " is not a known type"
    else:
        album.non_standard_album()



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Searches discogs DB and moves mp3 files to an iTunes folder")
    parser.add_argument("path", help="Argument must include full path to album, surrounded by double quotes")
    parser.add_argument("album", help="Argument must include album name, surrounded by double quotes")
    parser.add_argument("type", help="Valid arguments for album type are: standard, compilation, soundtrack, or single")
    parser.add_argument("--artist", default="Various", help="Argument must include artist name, surrounded by double quotes")



    args = parser.parse_args()
    main(args.path, args.album, args.type, args.artist)

