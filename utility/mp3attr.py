import eyed3
import os 
import sys

dirpath = sys.argv[1];
files = os.listdir(dirpath)

for idx, file in enumerate(files):

    num = idx + 1
    title = file[:-4]
    artist = 'Rhondabeat' if file != 'S.C.A.M.mp3' else 'Leon O. Rosén'

    print(file)

    tag = eyed3.load(os.path.join(dirpath, file)).tag
    tag.artist = artist
    tag.album = "Kitboga Remixes"
    tag.album_artist = artist
    tag.title = title
    tag.track_num = num

    tag.save()
    
    print('done')