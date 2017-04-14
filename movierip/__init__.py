#!/usr/bin/env python
# -*- coding: utf-8; mode: python; -*-

##  Copyright 2010–17 by Diedrich Vorberg <diedrich@tux4web.de>
##
##  All Rights Reserved
##
##  For more Information on orm see the README file.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program; if not, write to the Free Software
##  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##
##  I have added a copy of the GPL in the file LICENSE

import sys, os, os.path, optparse, lxml.etree, re, subprocess, types, urllib
from string import *
from cStringIO import StringIO
from t4.debug import log, debug
import tmdb3 as tmdb; tmdb.set_key("a888a20b801aeefde1ba41a932898d48")

options = None

def present_movie(idx, movie):
    print idx,
    if type(movie.releasedate) == types.UnicodeType:
        year = movie.releasedate
        
    elif not movie.releasedate:
        year = "unknown"
    else:
        year = str(movie.releasedate.year)
        
    print "%s (%s)" % ( movie.title, year, )

def search_tmdb_for_movie(title):
    """
    Run a search query on the tmdb for `title`.
    """
    global options
    
    name, year = name_and_year(title)

    if year is not None:
        result = tmdb.searchMovieWithYear("%s (%i)" % (name, year))

        movies = list(result)

        if year is not None:
            def year_match(movie):
                if movie is None:
                    return False
                else:
                    if not movie.releasedate:
                        return False
                    else:
                        y = movie.releasedate.year
                        return y == year or y == year - 1 or y == year + 1

            movies = filter(year_match, movies)
    else:
        result = tmdb.searchMovie(name)
        movies = list(result)

    if len(movies) == 0:
        raise Exception("No movie found: %s" % repr(name))

    elif len(movies) > 1:
        movies.sort(lambda a, b: cmp(str(a.releasedate), str(b.releasedate)))
        
        print        
        for idx, movie in enumerate(movies):
            present_movie(idx, movie)
        print
        
        if options is None or options.choose is None:
            print "Enter index [0]:",
            i = strip(raw_input())
            if i == "":
                idx = 0
            else:
                idx = int(i)
        else:
            idx = int(options.choose)
    else:
        idx = 0

    return movies[idx]

tmdb_id_re = re.compile(r"\d+")
def get_tmdb_movie_for(title):
    """
    Title can be either one of:
    • The 'Title' (string)
    • The 'Title (year)' (string)
    • tmdb id (integer)
    """    
    if type(title) == types.IntType or tmdb_id_re.match(title) is not None:
        try:
            return tmdb.Movie(int(title))
        except KeyError:
            raise Exception("Movie with tmdb %i not found." % int(title))
    else:    
        return search_tmdb_for_movie(title)

def info_from_tmdb_movie(movie):            
    if movie.tagline is None:
        movie.tagline = ""
        
    if movie.overview is None:
        movie.overview = ""

    if strip(movie.tagline):
        description = movie.tagline + \
            u" — " + movie.overview
    else:
        description = movie.overview

    # Download artwork
    if options is None or not options.art:
        url = movie.poster.geturl()
        rest, artfn = rsplit(url, "/", 1)
        artpath = os.path.join("/tmp", artfn)

        if not os.path.exists(artpath):
            jpeg = urllib.urlopen(url).read()
            fp = open(artpath, "w")
            fp.write(jpeg)
            fp.close()
            
        options.art = artpath

    info = { "song": movie.title,
             "description": description, }
    
    genres = movie.genres
    if len(genres) > 0:
        info["genre"] = genres[0].name
        
    if movie.releasedate:
        info["year"] = str(movie.releasedate.year)

    return info
    
def name_and_year(filename):
    """
    Attempt to parse a filename. Return a tuple a ( name, year, ).
    The year may be None, otherwise it's an integer.
    """
    filename_re = re.compile(r"(.*?)\.(\d+)\.\d+p.*")
    match = filename_re.match(filename)
    if match is not None:
        name, year = match.groups()
        name = replace(name, ".", " ")
        return ( name, int(year), )

    filename_re = re.compile(r"(.*?)\((\d+)\).*")
    match = filename_re.match(filename)
    if match is not None:
        name, year = match.groups()
        return ( strip(name), int(year),  )
    else:
        try:
            name, ext = split(filename, ".", 1)
        except ValueError:
            name = filename
        
        return ( strip(name), None, )

