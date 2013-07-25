movierip
========

A Python script that uses ffmpeg and the mp4v2 tools plus data from
themoviedb.com or thetvdb.com to create a neat, iTunes accepted .m4v
file for a movie.

I am in the process of “ripping” my entire collection of movie and
TV-show DVDs and BDs to harddrive to have them available in iTunes and
on my Apple TV. All my experience, tipps and quirks go into this script.

You'll need:
o Python 2.7 
o ffmpeg from http://www.ffmpeg.org
o mp4v2 tools from http://code.google.com/p/mp4v2/
o tmdb Python module, use easy_install tmdb
o tvdb_api Python module, use easy_install tvdb_api
o lxml Python module

This should be it.

Use

   movierip --help

but be warned, this thing's got about as many switches as ls. Here's
an example.

   movierip -e 1 -d 2 Lars\ and\ the\ Real\ Girl\ \(2007\).vob

The magic is in the file name: “Real Girl” is the movie's title and
it's been published in 2007, according to themoviedb.com. The script
will use that info to query the database and retrieve metadata. It the
query yields more than one movie, the script will ask which one to
pick. The -e is for English sound track, -d for German
(“deutsch”). Using --soundtrack LNG=# will expect a sound track for
language LNG in track #.

Combine a number of files using cat and pipe them into ffmpeg:

   cat VTS_01_1.VOB  VTS_01_2.VOB  VTS_01_3.VOB  \
       VTS_01_4.VOB  VTS_01_5.VOB  VTS_01_6.VOB  \
       VTS_01_7.VOB  VTS_01_8.VOB | \
       movierip --sd -d 1 -e 3 \
                -m song="Independence Day" -m year=1996 --choose 0 -

The “song” and “year” metainfo are used to identify the film on
themoviedb.com. The moviedb query returns more than on emovie for that
name and year and we “--choose” the first. German and English audio
tracks are converted.

    movierip -v -N -T 2 \
         -m type=tvshow -m show="The Simpsons" -m year=1989 \
         -e 1 S08E01.vob

Let's convert a Simpson's Episode. I've copied the VOB files off of
the DVD using Slysoft's CloneDVD Mobile. That makes it really easy to
overcome the convoluted data structure on the DVD, but it doesn't
allow me to copy more that one sound track. Sad, but can't be
helped. I supply show and year info on the command line using -m and
set the type to tvshow so movierip knows which database to query for
episode details and iTunes puts the resulting file in the right
category. -N lets ffmpeg be nice to other processes, -T limits the
number of concurrent ffmpeg threads to two instead of the default four
(so I can use the computer more comfortably during conversion) and -v
lets me see ffmpeg and utility command lines on the terminal.
     