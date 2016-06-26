#!/usr/bin/python3
import os
import random

pathFile = 'osu_songs_path.txt' # In the current directory, change path/name if u need
playlistFile = 'Osu! Playlist.m3u' # In the current directory, change path/name if u need
    

def check_osu_path_file():
    with open(pathFile, 'a+') as f:
        print("Checking file ...")
        f.seek(0)
        songPath = f.read()
        if os.path.isdir(songPath):
            songPath = os.path.join(songPath, '') # Add ending slash if not already
            f.seek(0)
            f.truncate()
            f.write(songPath)
            print("osu! songs path detected: {}".format(songPath))
            scan_folder(songPath) # Let's scan
            
        else:
            print("The osu! songs path is invalid, please change it in file '{}'.".format(pathFile))


def scan_folder(songPath):
    print("Scanning folder ...")
    folderArray = (os.listdir(songPath))
    trash = "Failed"
    if trash in folderArray: folderArray.remove(trash)
    totalSong = len(folderArray)
    print("There are {} songs in the folder.".format(totalSong))
    print("Do you want to randomize the order?")
    askRandom = input("Enter 'y' if yes, others if not. ").lower()
    
    if askRandom == 'y':
        random.shuffle(folderArray)
        print("The order has been randomized.")
    
    print("Please wait, it could takes much time depend on your number of songs ...")
    
    with open(playlistFile, 'w') as f:
        for folder in folderArray:
            currentPath = os.path.join(songPath + folder, '')
            songFile = currentPath + get_song(currentPath)
            f.write(songFile + "\n")

    print("Done. File '{}' is successfully written.".format(playlistFile))
    print("Please move and/or open the file depend on your music player.")

def get_song(currentPath):
    found = False
    for folderFiles in os.listdir(currentPath):
        if folderFiles.endswith('.osu') and not found:
            with open(currentPath + folderFiles, 'r', encoding="utf-8") as osu:
                for i, line in enumerate(osu):
                    if i == 3:
                        songFileName = line[15:-1]
                        found = True
                        return songFileName

        elif found: break

check_osu_path_file()

input("\nPress any key to quit...\n")