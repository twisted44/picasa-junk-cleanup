# picasa-junk-cleanup
> Cleanup files/folders leftover by the now defunct Picasa Photos by Google.

Picasa Photos has been discontinued by Google.  It was a solid program to manage large
photo libraries.  Google has migrated to Google Photos, and provided support to updoad
photo libraries using Google Backup and Sync.  Unfortunately, backup and sync does not
respect that people migrating from Picasa may end up with many duplicate photos on
Google Photos due to the automatic uploading of the original photo files stored by
Picasa under .picasaoriginals folder.

This script searches for all .picasaoriginal folders and moves them to an archive of
the user's choice.  This allows Backup and Sync to work normally.


## picasa-junk-cleanup 
> This is the main script.
This script will find all .picasaoriginal folders under a given path (start_dir) 
and move them (including contents) to a new archive location (archive_dir).

If there is a .picasaini file at the _same_ location, it will also be moved.

If there are .picasaini files in _other_ locations they will _not_ be moved.


### Usage example

picasa-junk-cleanup

To create a log file, redirect output with 
picasa-junk-cleanup |& tee -f logfile

### picasa-zip-cleanup 
> This is a small utility to cleanup older type archives (picasa.zip).
This script will find all picasa.zip files and move them to the same archive.


## Meta

Martin Parley – twisted44@yahoo.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/twisted44] (https://github.com/twisted44/)





## Other Notes
In Linux Shell, use these handy find commands:

### Find all DIRECTORIES with picasa in the name (includes hidden)
> find . -type d -name *picasa*

### Find all FILES with picasa in the name (includes hidden)
> find . -type f -name *picasa*
