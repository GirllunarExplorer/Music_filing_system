Music_filing_system
===================

Takes mp3 files, creates folders for them in iTunes media folder, and renames the files based on discogs directory

The program takes four arguments: a source path, album name, artist name and album type.  Album types are "standard", "compilation", "soundtrack", and "single".  If no artist is specified, the default is "Various" which is what Discogs sets as the artist label for compilations and soundtracks.  So for example:

python MusicMove.py --artist "Gin Wigmore" "/Users/usernam/eDesktop/Gin Wigmore/Gravel And Wine" "Gravel And Wine" standard

or 

python MusicMove.py "/Users/username/Desktop/28 Days Later Soundtrack" "28 Days Later (The Soundtrack Album)" soundtrack

>>>Please enter destination path.  Default is /Users/username/Music/iTunes/iTunes Media/Music/

Because discogs limits the amount of tokens given out in a 24 hour period, each user must use a new key every time the program is run:

>>>follow this url to authorize the client
http://www.discogs.com/oauth/authorize?oauth_token=hxSKSosFwywjQAlqobcgXNCpJGtSHbgDLiSjUScz

SLIbiFDlVx

The program searches through each release that matches the album name and asks the user if that is the correct release:

>>><Track u'1' u'The Beginning'>
>>><Track u'2' u'Rage'>
>>><Track u'3' u'The Church'>
>>><Track u'4' u"Jim's Parents (Abide With Me)">
>>><Track u'5' u'Then There Were 2'>
>>><Track u'6' u'Tower Block'>
>>><Track u'7' u'Taxi (Ave Maria)'>
>>><Track u'8' u'The Tunnel'>
>>><Track u'9' u'AM180'>
>>><Track u'10' u'An Ending (Ascent)'>
>>><Track u'11' u'No More Films'>
>>><Track u'12' u"Jim's Dream">
>>><Track u'13' u'In Paradisum'>
>>><Track u'14' u"Frank's Death - Soldiers (Requiem In D Minor)">
>>><Track u'15' u"'I Promised Them Women'">
>>><Track u'16' u'The Search For Jim'>
>>><Track u'17' u'Red Dresses'>
>>><Track u'18' u'In The House - In A Heartbeat'>
>>><Track u'19' u'The End'>
>>><Track u'20' u'Season Song'>
>>><Track u'21' u'End Credits'>
>>>does this look correct?

yes

>>>going to use <Master 113964 u'28 Days Later (The Soundtrack Album)'>


If it is a standard album, the files from the source should move automatically to the destination folder, but compilations and soundtracks require the user to input the artist name for each track, in order to create a "artist - song.file" format:


>>>who is the artist for The Beginning

John Murphy

>>>Moving to /Users/username/Music/iTunes/iTunes Media/MusicSoundtracks/28 Days Later (The Soundtrack Album)/John Murphy - The beginning.mp3

