#!/usr/bin/env python
# -*- coding: utf-8 -*-
# picasa_zip_cleaner


"""
#############################################################################
CHANGELOG
  version 1.0 - 5/17/2020
    After the main cleanup (picasa-junk-cleanup), there were som picasa.zip 
    files leftover too (from an older cleanup strategy).
    This script will move those files to the same archive.

DESCRIPTION

 Utility to move picasa.zip to archives, retaining the folder structure
 Main script for cleaning up files left behind by Picasa Photo Editor.

#############################################################################
"""

import time
import os
from os.path import  dirname
from shutil import move
from pathlib import Path
from picasa-cleanup-functions import countdown_in_sec, confirm

start_dir = "c:\\Photos\\"
archive_dir = "c:\\Photos_PicasaOriginals\\"
#archive_dir = "c:\\__test__archive\\"
#start_dir = "c:\\Photos Cleanup\\PhotosTest2\\"

simulation_mode = False



list_of_pzip_paths = []
keyword = '.picasa.zip'


print("\n\nThis script will cleanup the .picasa.zip")
print("...\n")


# Build list of ALL picasa zip files
for dirpath, dirnames, files in os.walk(start_dir):
    for f in files:
        if f == keyword:
            pz_path = join(dirpath, keyword)
            list_of_pzip_paths.append(pz_path)




if not list_of_pzip_paths:
    raise SystemExit('No Picasa zip files found')
print("\nList of all PICO ZIP files:")
print(*list_of_pzip_paths, sep="\n", end="\n")


# Prompt user, then perform the ZIP and DELETE process
if True:
    print("\n\n  >>> Are you sure you want to *ARCHIVE* and *DELETE* all PICO PATHS?")
    if confirm("Type y to continue, or n to quit:  ") is False:
        raise SystemExit("No worries, better safe than sorry!\n")
    print("Ok.  Here we go ...\n")
    countdown_in_sec(2)


# Move picasa.zip to the archive, retain the folder structure
for pz in list_of_pzip_paths:

    print("Now working on ", pz)

    # Replace the partial path from start_dir to archive_dir
    pz_new = pz.replace(start_dir, archive_dir)

    # If it doesn't find start_dir as part of d, then abort (this should never happen)
    if ( pz_new == pz ):
        raise SystemExit(f'No suitable subsitution to create a new path in {pz}')

    # If the directory doesn't already exist, create it (otherwise move won't work)
    pz_dirname = dirname(pz_new)
    if isdir(pz_dirname):
        print('DIR Already exists:  ', pz_dirname)
    else:
        print('Making new dir:  ', pz_dirname)
        try:
            Path(pz_dirname).mkdir(parents=True, exist_ok=True)
        except Exception as ex:
            raise(ex)
    if True: print("*-------  ", pz_new)


    if simulation_mode:
        print('SIM ONLY... not moving file')
    else:
        try:
            move(pz, pz_new)
        except Exception as ex:
            raise(ex)

    print()
print()



if __name__ == "__main__":
   print()