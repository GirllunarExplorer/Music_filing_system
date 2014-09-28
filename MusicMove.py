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



def main(album_path, artist_name, album_name):




    print 'working on', album_path
    title = album_path.split('/')[-1]

    itunes_path = '/Users/tracyrohlin/Music/iTunes/iTunes Media/Music/'

    if not os.path.exists(itunes_path + artist_name):
        os.mkdir(itunes_path + artist_name)
    itunes_path += artist_name + '/'
    if not os.path.exists(itunes_path + album_name):
      os.mkdir(itunes_path + album_name)
    itunes_path += album_name + '/'

    client = discogs.Client('test client')
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


    for track in target_album.tracklist:
        for song in os.listdir(album_path):
            #print track.title
            if track.title in song:
                shutil.copyfile(album_path+'/'+song, itunes_path+'/'+string.capwords(track.title)+'.mp3')
                print (album_path+'/'+song, itunes_path+'/'+string.capwords(track.title)+'.mp3')





if __name__ == '__main__':

    if len(sys.argv) == 4:
        main(*sys.argv[1:])



    else:
        print 'Argument must be full path to album, surrounded by double quotes'
        sys.exit(1)


