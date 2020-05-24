#!/usr/bin/env python
# -*- coding: utf-8 -*-
# picasa_junk_cleaner2


"""
#############################################################################
CHANGELOG
  version 2.0 - 5/11/2020
    Instead of surgically finding and zipping all junk folders,
    make a copy of all junk to a different location on disk,
    then delete all junk!
    Maintain folder structure in new archive location.

DESCRIPTION

 Main script for cleaning up files left behind by Picasa Photo Editor.

 The primary junk is a folder named .picasaoriginals/ that contains originals images
 unmodified by Picasa.  These files will cause duplicate images when the folder is
 uploaded to Google Photos (using Google Backup and Sync).

 There is another junk file named picasa.ini which may or may not exist.  Confirmed
 it does not have any impact on Google Photos.  It will be archived, too.

 Implementation...
 1)  User inputs a starting directory (currently hardcoded as start_dir).
 2)  User inputs an archive directory (currently hardcoded as arch_dir).
 3)  Walk through all start_dir subfolders and store path of any junk (folders/files).
 4)  For each folder, copy or move junk to archive (aslo do .ini file).
     NOTE.  There may be .picasa.ini files without the folder, and they will need
     to be removed later (manually)
 4)  CAREFUL!  Prompt user before doing batch ZIP/DELETE.
 5)  Delete original junk!

TODO
 - add user inputs
 -   Starting directory
 -   simulation mode (npo zip, no delete)
 - add option (or just small utility) to delete empty folders (only contain .picasaorig and .ini)
 - notify if there are folders that only contain .mp4, .mov, .vid, etc.

#############################################################################
"""

import os
import time
from os.path import  dirname
from picasa_cleanup_functions import countdown, countdown_in_sec, \
                         build_list_of_pico_paths, \
                         check_for_multiple_layers_of_junk, \
                         confirm, \
                         delete_pico_path_and_picini, \
                         copy_pico_path_and_picini_to_archive_dir

#def main():

# Set starting point
#start_dir = "c:\\Photos\\2015\\"
#start_dir = "c:\\Photos\\"
#start_dir = "c:\\PhotosTestLayers\\"
#start_dir = "c:\\Photos\\"
#start_dir = "c:\\PhotosTest\\"
#start_dir = "c:\\Photos Cleanup\\PhotosTest2\\"
#start_dir = "c:\\Photos Cleanup\\PhotosTest\\"
#archive_dir = "c:\\__test__archive\\"
# Production values... don't use until you're really ready
start_dir = "c:\\Photos\\"
archive_dir = "c:\\Photos_PicasaOriginals\\"
simulation_mode = True

# Other variables
list_of_pico_paths = []
ignore_list = []

print("\n\nThis script will cleanup junk left behind by Picasa.")
print("You may need to remove .picasa.ini folders manually.\n")
print("...\n")
time.sleep(1)


# Get list of ALL folders below starting dir that have the .picasaoriginals sub-folder
list_of_pico_paths = build_list_of_pico_paths(start_dir)
if not list_of_pico_paths:
    raise SystemExit('No Picasa junk folders found')
print("\nList of all PICO PATHS:")
print(*list_of_pico_paths, sep="\n", end="\n")


# Prompt user, then perform the ZIP and DELETE process
if True:
    print("  >>> Are you sure you want to *ARCHIVE* and *DELETE* all PICO PATHS?")
    if confirm("Type y to continue, or n to quit:  ") is False:
        raise SystemExit("No worries, better safe than sorry!\n")
    print("Ok.  Here we go ...\n")
    countdown_in_sec(2)


# Proceed with COPY stuff
for d in list_of_pico_paths:

    # Printing for debug
    if True: print("********  ", d)

    # Copy d to new path
    # c:\Photos Cleanup\PhotosTest\2026\FolderB\.picasaoriginals
    # c:\__test__archive\2026\FolderB\.picasaoriginals
    # What is new path?

    # Replace the partial path from start_dir to archive_dir
    new_home = d.replace(start_dir, archive_dir)

    # If it doesn't find start_dir as part of d, then abort (this should never happen)
    if ( new_home == d ):
        raise SystemExit(f'No suitable subsitution in {d}')


    copy_pico_path_and_picini_to_archive_dir(d, new_home, simulation_mode)

    print()
print()

# Proceed to DELETE junk
for d in list_of_pico_paths:

    # Printing for debug
    if True: print(" X X X X X X X X X ", d)

    # Delete pico path
    # c:\Photos Cleanup\PhotosTest\2026\FolderB\.picasaoriginals
    delete_pico_path_and_picini(d, simulation_mode)

    print()
print()


if __name__ == "__main__":
   print()