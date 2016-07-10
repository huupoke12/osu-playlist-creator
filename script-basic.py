#!/usr/bin/python3
import os
import random
import shutil

# Change path/name if u need
pathFile = 'osu_songs_path.txt'
playlistFile = 'Osu! Playlist.m3u'
extractPath = 'Osu! Extracted Songs'
extractPath = os.path.join(extractPath, '')
listOutput = 'extracted_songs.txt'
playlistOutputSongs = 'Osu! Songs Extracted.m3u'
currentFolderAbsPath = os.path.abspath('')
currentFolderAbsPath = os.path.join(currentFolderAbsPath, '')

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
    
    choose = input("\nDo you want to extract(copy) ALL your songs (it will take much time) (enter 'c') OR \njust want to create the playlist file (enter others)?\n").lower()
    
    if choose == 'c': extract_song(songPath, folderArray, totalSong)
    else: create_playlist(songPath, folderArray, totalSong)

def create_playlist(songPath, folderArray, totalSong):
    print("Do you want to randomize the order?")
    askRandom = input("Enter 'y' if yes, others if not: ").lower()
    
    if askRandom == 'y':
        random.shuffle(folderArray)
        print("The order has been randomized.")
    
    print("Creating playlist file, please wait, it could takes much time depend on your number of songs ...")
    
    with open(playlistFile, 'w') as f:
        for i, folder in enumerate(folderArray):
            show_percent(i + 1, totalSong)
            currentPath = os.path.join(songPath + folder, '')
            songFile = currentPath + get_song(currentPath)
            f.write(songFile + "\n")

    print("\nDone. File '{}' was successfully written.".format(playlistFile))
    print("Please move and/or open the file depend on your music player.")

def extract_song(songPath, folderArray, totalSong):
    allowContinue = True
    if os.path.isdir(extractPath):
        print("There is already a folder named '{}', do you want to delete and recreate it?".format(extractPath))
        askDelete = input("Enter 'y' if yes, others if not: ")
        if askDelete == 'y':
            print("Deleting folder '{}' ...".format(extractPath))
            shutil.rmtree(extractPath)
            allowContinue = True
        else:
            print("Ok, just handle it yourself.")
            allowContinue = False
            return None
            
        
    if allowContinue:
        
        
        print("Creating folder '{}' ...".format(extractPath))
        os.makedirs(extractPath)
        print("Copying to folder '{}'. Please wait, it could take much time depend on the number of songs ...".format(extractPath))
        
        with open(listOutput, 'w') as list, open(playlistOutputSongs, 'w') as playlist:
            for i, folder in enumerate(folderArray):
                show_percent(i + 1, totalSong)
                currentPath = os.path.join(songPath + folder, '')
                songFile = currentPath + get_song(currentPath)
                details = get_song_details(folder)
                extension = os.path.splitext(songFile)[-1]
                songEditedName = details[0] + " - " + details[1]
                copiedSongFile = songEditedName + extension
                shutil.copyfile(songFile, extractPath + copiedSongFile)
            
                list.write(copiedSongFile + "\n")
                playlist.write(currentFolderAbsPath + extractPath + copiedSongFile + "\n")
            
        print("\nDone. The songs is in '{}'".format(extractPath))
        print("The list of extracted songs is '{}'".format(listOutput))
        print("The playlist file named '{}'. You can copy it to playlist folder, depends on the music player".format(playlistOutputSongs))
        

def get_song_details(folderName):
    splitSpace = folderName.split(' ')
    if splitSpace[0].isdigit(): splitSpace.pop(0)
    rawDetail = ' '.join(splitSpace)
    detailArray = rawDetail.split(' - ')
    title = detailArray[1].strip()
    artist = detailArray[0].strip()
    return [title, artist]

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

def show_percent(now, total):
    percent = round(now/total * 100)
    print("Processing {}/{} ({}%). Please wait ...".format(now, total, percent), end='\r')
    

check_osu_path_file()

input("\nPress enter key to quit...\n")