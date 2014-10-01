__author__ = 'tracyrohlin'

import sys
import re
import os.path
import os
import discogs_client as discogs
import os
import shutil
import string

discogs.user_agent = 'MyMusicPythonProject'

def main(album_path, artist_name, album_name, album_type):
    client = discogs.Client('test client')

    print 'working on', album_path
    title = album_path.split('/')[-1]

    itunes_path = '/Users/tracyrohlin/Music/iTunes/iTunes Media/Music/'

    releases = [x for x in client.search(album_name, artist = artist_name)]
    target_album = None

    while releases and not target_album:
        current = releases.pop()
        for track in current.tracklist:
            print track
        print "does this look correct?"
        answer = raw_input()
        if answer =="yes":
            target_album = current
    print "going to use", target_album

    if album_type == 'standard':

        if not os.path.exists(itunes_path + artist_name):
            os.mkdir(itunes_path + artist_name)
        itunes_path += artist_name + '/'
        if not os.path.exists(itunes_path + album_name):
            os.mkdir(itunes_path + album_name)
        itunes_path += album_name + '/'

        for track in target_album.tracklist:

            for song in os.listdir(album_path):
                if track.title in song:
                    shutil.copyfile(album_path+'/'+song, itunes_path+'/'+string.capwords(track.title)+'.mp3')
                    print (album_path+'/'+song, itunes_path+'/'+string.capwords(track.title)+'.mp3')

    elif album_type == "compilation":

        if not os.path.exists(itunes_path + "Compilations"):
            os.mkdir(itunes_path + "Compilations")
        itunes_path += "Compilations" + '/'
        if not os.path.exists(itunes_path + album_name):
            os.mkdir(itunes_path + album_name)
        itunes_path += album_name + '/'

        for track in target_album.tracklist:
            print "who is the artist for " + track.title
            compilation_artist = raw_input()
            for song in os.listdir(album_path):
                print "Is this the correct title track? " + song

                if raw_input() == "yes":
                    #Will not accept foreign characters, inclusing characters with accent marks on them
                    shutil.copyfile(album_path+'/'+ song, itunes_path  + compilation_artist + " - " + string.capwords(track.title)+'.mp3')
                    break

    elif album_type == "soundtrack":
        if not os.path.exists(itunes_path + "Soundtrack"):
            os.mkdir(itunes_path + "Soundtrack")
        itunes_path += "Soundtrack" + '/'
        if not os.path.exists(itunes_path + album_name):
            os.mkdir(itunes_path + album_name)
        itunes_path += album_name + '/'

        for track in target_album.tracklist:
            print "who is the artist for " + track.title
            compilation_artist = raw_input()
            for song in os.listdir(album_path):
                print "Is this the correct title track? " + song

                if raw_input() == "yes":
                    #Will not accept foreign characters, inclusing characters with accent marks on them
                    shutil.copyfile(album_path+'/'+ song, itunes_path  + compilation_artist + " - " + string.capwords(track.title)+'.mp3')
                    break

    elif album_type == "single":
        if not os.path.exists(itunes_path + "Singles"):
            os.mkdir(itunes_path + "Singles")
        itunes_path += "Singles" + '/'
        if not os.path.exists(itunes_path + artist_name):
            os.mkdir(itunes_path + artist_name)
        itunes_path += artist_name + '/'

        for track in target_album.tracklist:
            print "who is the artist for " + track.title
            compilation_artist = raw_input()
            for song in os.listdir(album_path):
                if track.title in song:
                    shutil.copyfile(album_path+'/'+song, itunes_path+'/'+string.capwords(track.title)+'.mp3')

    else:
        print album_type + " is not a known type"

if __name__ == '__main__':

    if len(sys.argv) == 5:
        main(*sys.argv[1:])

    else:
        print 'Argument must include full path to album, surrounded by double quotes'
        print "Argument must also include artist name, album name, and album type"
        print "Valid arguments for album type are: standard, compilation, soundtrack, or single"
        sys.exit(1)



