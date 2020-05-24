# picasa-junk-cleanup
> Cleanup files/folders leftover by the now defunct Picasa Photos by Google.

[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]

Picasa Photos has been discontinued by Google.  It was a solid program to manage large
photo libraries.  Google has migrated to Google Photos, and provided support to updoad
photo libraries using Google Backup and Sync.  Unfortunately, backup and sync does not
respect that people migrating from Picasa may end up with many duplicate photos on
Google Photos due to the automatic uploading of the original photo files stored by
Picasa under .picasaoriginals folder.

This script searches for all .picasaoriginal folders and puts them into a .picasa.zip
file at the same location.  This allows Backup and Sync to bypass the duplicate photos
if is selected in Preferences -> Change -> Backup Photos and Videos (instead of all
files.)

![](header.png)


## picasa-junk-cleanup 
This is the main script.
This script will find all .picasaoriginal folders under a given path (start_dir) 
and move them (including contents) to a new archive location (archive_dir).

If there is a .picasaini file at the _same_ location, it will also be moved.

If there are .picasaini files in _other_ locations they will _not_ be moved.


## Usage example

picasa-junk-cleanup

To create a log file, redirect output with 
picasa-junk-cleanup |& tee -f logfile


## Meta

Martin Parley – twisted44@yahoo.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/twisted44] (https://github.com/twisted44/)





## Other Notes

In Linux Shell, use these handy find commands:

# Find all DIRECTORIES with picasa in the name (includes hidden)
find . -type d -name *picasa*


# Find all FILES with picasa in the name (includes hidden)
find . -type f -name *picasa*