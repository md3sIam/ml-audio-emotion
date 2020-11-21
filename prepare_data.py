from py7zr import SevenZipFile
from os import getcwd, path, mkdir
from shutil import rmtree

DATA_DIR = path.join(getcwd(), 'Data')

if path.isdir(DATA_DIR):
    if input("Data folder exist. Unpack data again? [Y/n]: ")[0].lower() in ['y', 'н']:
        rmtree(DATA_DIR, ignore_errors=True)
    else:
        exit()

mkdir(DATA_DIR)

print('Opening the archive')
with SevenZipFile('Data.7z') as zipped_data:
    print('Unpacking...')
    zipped_data.extractall(path=DATA_DIR)
print('Done')
