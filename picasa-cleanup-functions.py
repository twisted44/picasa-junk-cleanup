# -*- coding: utf-8 -*-

"""Function definitions for picasa_junk_cleaner"""

import os
import time
from os.path import join, isdir, isfile, basename, dirname
from shutil import rmtree, copytree, copyfile
from send2trash import send2trash

keyword = ".picasaoriginals"


#----------------------------------------------------------------------------
def build_list_of_pico_paths(pdir):
    """Return list of photo directories containing picasa junk."""
    dir_list = []
    for dirpath, dirnames, files in os.walk(pdir):
        for d in dirnames:
            if d == keyword:
                #print("Found one:  ", dirpath)
                pico_path = join(dirpath, keyword)
                dir_list.append(pico_path)
    return dir_list
#----------------------------------------------------------------------------
def check_for_multiple_layers_of_junk(pdir):
    """Look for multiple layers of junk for pdir, return True if found.

    Multiple layers can be:
    1) Any dirpath containing the .picasaoriginals folder AND other folders
    2) Any dirpath containing multiple layers of .picasaoriginals folders
    """

    for dirpath, dirnames, files in os.walk(pdir):

        # If there are 2 or more folders, and one is .picasaoriginals
        if len(dirnames) > 1 and keyword in dirnames:
            return True

        # If there are 2 or layers of .picasaoriginals
        if basename(dirpath) == keyword and keyword in dirnames:
            return True

    return False
#----------------------------------------------------------------------------
def confirm(prompt=None, resp=False):
    """Prompt user for yes or no response. Returns True for yes and False for no.

    "resp" should be set to the default value assumed by the caller when
    user simply types ENTER.

    Ex.
    >>> confirm( prompt="Create Directory?", resp=True )
    Create Directory? [y]|n:
    True
    >>> confirm(prompt="Create Directory?", resp=False)
    Create Directory? [n]|y:
    False
    >>> confirm(prompt="Create Directory?", resp=False)
    Create Directory? [n]|y: y
    True
    """

    if prompt is None:
        prompt = "Confirm"

    if resp:      # If default response is True, bracket the [y]
        prompt = "%s [%s]|%s: " % (prompt, "y", "n")
    else:        # If default response is True, bracket the [n]
        prompt = "%s [%s]|%s: " % (prompt, "n", "y")


    while True:
        ans = input(prompt)
        if not ans:
            return resp
        if ans not in ('y', 'Y', 'n', 'N'):
            print("please enter y or n.")
            continue
        if ans in ('y', 'Y'):
            return True
        if ans in ('n', 'N'):
            return False
#----------------------------------------------------------------------------
def restore():
    fresh_data = "c:\\Photos Cleanup\\PhotosTestUntouched\\"
    test_data  = "c:\\Photos Cleanup\\PhotosTest2\\"

    print(f'FRESH {fresh_data}')
    print(f'TEST  {test_data}')

    print(f"Restoring data from {fresh_data} to {test_data} ...")
    if isdir(test_data):
        print("\nFirst, delete the existing test_data")
        rmtree(test_data)
        print("OK")
    else:
        print("\nTest_data does not exist.. continue.")

    print("\nThen, copy the fresh data to test data")
    copytree(fresh_data, test_data)
    print("OK")
    print("\nDone\n")

#---------------------------------------------------------------------------
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = "{:02d}:{:02d}".format(mins, secs)
        print(timeformat, end="\r")
        time.sleep(1)
        t -= 1
    print("Blastoff!!!\n\n")

#---------------------------------------------------------------------------
def countdown_in_sec(s):
    while s:
        timeformat = "{:02d}".format(s)
        print(f"{timeformat} -> ", end="\r",flush=True)
        time.sleep(1)
        s -= 1
    print("Blastoff!!!\n\n")
    time.sleep(.75)

#----------------------------------------------------------------------------
def copy_pico_path_and_picini_to_archive_dir(pico_dir, arch_dir, sim=False):
    """Copy the .picasaoriginals/ folder and the .picasasa.ini file at the same place
    to it's new home in the archive directory
    Returns name of new zip file on success, or False on failure.
    """
    ini_file = pico_dir.replace( keyword, '.picasa.ini' )
    # Double-check that replacement worked
    if ( ini_file == pico_dir ):
        #print(f"\nERROR: Could not create .picasa.ini from {pico_dir}")
        #return False
        raise SystemExit(f"Did not correctly create a new .ini file: {ini_file}")

    arch_ini = dirname(arch_dir)

    # Print verbose messages to screen (modify to False to disable)
    if True:
        print("============  INFO  ============")
        print("-  pico_dir:     ",pico_dir)
        print("-  ini_file:     ",ini_file)
        print("-  arch_dir:     ",arch_dir)
        print("-  ini_arch:     ",arch_ini)
        print("================================")

    # Double-check that .picasaoringals folder is actually here.
    # It should never be missing if the ignore_list and zippy_list are working.
    if isdir( pico_dir ) is False:
        print("\nERROR: No .picasaoriginals/ folder here. Skipping.\n", pico_dir)
        return False

    # Add the top-level picasa.ini if it exists
    if isfile( ini_file ) is False:
        print("No .ini file here.. continuing anyway")

    # If simulation mode is True, don't do anything
    if sim:
        print("**SIMULATION MODE**  _NOT_ doing any copy/move operations)")
        return True


    # Check to see if arch_dir already exists (will cause copytree to fail)
    if ( isdir(arch_dir) ):
        raise SystemExit(f'arch_dir already exists...aborting')

    # Recursively copy the pico_dir to the arch_dir
    print("copytree(pico_dir, arch_dir)")
    try:
        copytree(pico_dir, arch_dir)
    except:
        raise SystemExit(f'Cannot perform copytree on \n{arch_dir}')

    # Also copy the ini_file to the same place as the pico_dir
    if isfile( ini_file ):
        arch_ini = join( dirname(arch_dir), basename(ini_file) )

        if ( isfile( arch_ini) ):
            raise SystemExit(f'A new ini file already exists! {arch_ini}')

        print("copyfile(ini_file, arch_ini)")
        try:
            copyfile(ini_file, arch_ini)
        except:
            print("ERROR using copy on ini file!")

    return True
#----------------------------------------------------------------------------
def delete_pico_path_and_picini(pico_dir, sim=False):
    """Delete .picasaoriginals/* and .picasa.ini"""

    ini_file = pico_dir.replace( keyword, '.picasa.ini' )
    if ( ini_file == pico_dir ):
        raise SystemExit(f"Did not correctly create a new .ini file: {ini_file}")

    # Make sure the pico_dir still exists.. if not, something went horribly wrong.
    if isdir(pico_dir) is False:
        #print("Uh-oh. Something went wrong. Dir to delete no longer exists.")
        #print(pico_dir)
        #return False
        raise SystemExit(f'The pico_dir does not exist for deletion! {pico_dir}')

    # Ensure we have the permissions to delete (write)
    if os.access(pico_dir, os.W_OK) is False:
        #print("Uh-oh. Don't have permission to delete dir:\n", pico_dir)
        #return False
        raise SystemExit(f'No write permission, cannot delete {pico_dir}')

    if sim:
        print(f"xxxx SIMULATION MODE xxxx   ... NOT deleting {pico_dir}")
    else:
        print(f"DELETING {pico_dir}")
        #rmtree(pico_dir)
        try:
            send2trash(pico_dir)
        except Exception as ex:
            raise(ex)

    # See if the .picasa.ini file exists
    # Since this file is optional, no need to cause alarm if it does not exist
    if isfile(ini_file) is False:
        print(f"There is no ini file to delete here")
        # do not return anything since ini is optional
    elif os.access(ini_file, os.W_OK) is False:
        print(f"Uh-oh. Don't have permission to delete {ini_file}")
        # do not return anything since ini is optional
    elif sim:
        print(f"xxxx SIMULATION MODE xxxx  ... NOT deleting {ini_file}")
    else:
        print(f"DELETING {ini_file}")
        #os.remove( ini_file )
        # do not return anything since ini is optional
        try:
            send2trash(ini_file)
        except Exception as ex:
            print(ex)



    return True
#----------------------------------------------------------------------------
def copy_pzip_to_archive_dir(pz, new_pz, sim=False):
    """Copy the .picasa.zip file to to it's new home in the archive directory"""

    # Print verbose messages to screen (modify to False to disable)
    if True:
        print("============  INFO  ============")
        print("-  pz:     ",    pz)
        print("-  new_pz:     ",new_pz)
        print("================================")

    # If simulation mode is True, don't do anything
    if sim:
        print("**SIMULATION MODE**  _NOT_ doing any copy/move operations)")
        return True


    # Check to see if arch_dir already exists (will cause copytree to fail)
    if ( isdir(arch_dir) ):
        raise SystemExit(f'arch_dir already exists...aborting')

    # Recursively copy the pico_dir to the arch_dir
    #print("copytree(pico_dir, arch_dir)")
    #try:
#        copytree(pico_dir, arch_dir)
#    except:
#        raise SystemExit(f'Cannot perform copytree on \n{arch_dir}')

    # Also copy the ini_file to the same place as the pico_dir
#    if isfile( ini_file ):
#        arch_ini = join( dirname(arch_dir), basename(ini_file) )
#
#        if ( isfile( arch_ini) ):
#            raise SystemExit(f'A new ini file already exists! {arch_ini}')
#
#        print("copyfile(ini_file, arch_ini)")
#        try:
#            copyfile(ini_file, arch_ini)
#        except:
#            print("ERROR using copy on ini file!")

    return True

#----------------------------------------------------------------------------


if __name__ == "__main__":
    print()