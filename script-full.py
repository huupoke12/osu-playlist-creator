#!/usr/bin/python3
import os
import random
import mutagen.mp3

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
        f.write("#EXTM3U\n\n")
        for folder in folderArray:
            currentPath = os.path.join(songPath + folder, '')
            songFile = currentPath + get_song(currentPath)
            details = get_song_details(folder)
            title = details[0]
            artist = details[1]
            audio = mutagen.mp3.MP3(songFile)
            length = round(audio.info.length)
            f.write("#EXTINF:" + str(length) + "," + title + " - " + artist + "\n")
            f.write(songFile + "\n\n")

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
                        
                    elif i > 3: break

        elif found: break

def get_song_details(folderName):
    splitSpace = folderName.split(' ')
    if splitSpace[0].isdigit(): splitSpace.pop(0)
    rawDetail = ' '.join(splitSpace)
    detailArray = rawDetail.split('-')
    title = detailArray[1].strip()
    artist = detailArray[0].strip()
    return [title, artist]


check_osu_path_file()

input("\nPress any key to quit...\n")