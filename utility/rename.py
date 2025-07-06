import os
import sys

dryrun = True
dirpath = sys.argv[1]
files = os.listdir(dirpath)

files.sort(key=lambda file: os.path.getctime(os.path.join(dirpath, file)))

for idx, file in enumerate(files):
    name = os.path.basename(file)
    title = name.split('-')[1].strip()
    nbr = f'{idx+1}'.zfill(2)
    
    newname = f'{nbr} - {title}'
    
    print(newname)
    
    if not dryrun:
        os.rename(os.path.join(dirpath, name), os.path.join(dirpath, newname))
        print('done!')
