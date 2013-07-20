movierip
========

A Python script that uses ffmpeg and the mp4v2 tools plus data from
themoviedb.com or thetvdb.com to create a neat, iTunes accepted .mp4
file for a movie.

You'll need:
o Python 2.7 
o ffmpeg from http://www.ffmpeg.org
o mp4v2 tools from http://code.google.com/p/mp4v2/
o tmdb Python module, use easy_install tmdb
o tvdb_api Python module, use easy_install tvdb_api

This should be it.

Use

   movierip --help | less

but be warned, this thing's got about as many switches as ls. Here's
an example.

   movierip -e 1 -d 2 Lars\ and\ the\ Real\ Girl\ \(2007\).vob

The magic is in the file name: “Real Girl” is the movie's title and
it's been published in 2007, according to themoviedb.com. The script
will use that info to query the database and retriece metadata. It the
query yields more than one movie, the script will ask which one to
pick. The -e is for English sound track, -d for German
(“deutsch”). Using --soundtrack LNG=# will expect a sound track for
language LNG in track #.
   
