import os
import sys
import subprocess
import cPickle as pickle

def rename(directory, tag): #rename audio files and save the name change log as pickle
    fileslist = os.listdir(directory)
    newfileslist=map(lambda i: tag+ '_' + str(i) + '.' + fileslist[i].split('.')[1],range(len(fileslist)))
    log = zip(fileslist,newfileslist)
    with open( 'renamed_'+tag+'.pkl', "w" ) as f:
        pickle.dump(log, f)
    print directory
    for old, new in log:
        os.rename(directory+'/'+old,directory+'/'+new)
    print 'rename done'

def convertToWav(directory):
    audioFormats = ['mp3', 'flac', 'ogg', 'aiff', 'aif']
    filesList = os.listdir(directory)
    bashCommandlist = filter(None, map(lambda name: 'ffmpeg -i '+ directory + '/'+ name + ' -ar 22050 -ac 1 '+ directory+'/'+ name.split('.')[0]+'.wav' if str(name.split('.')[1]) in audioFormats else None, filesList))

    print "Converting all files to .wav format..."
    for command in bashCommandlist:
        subprocess.check_output(['bash','-c', command])
    print '.wav convert done.'

def movewavfiles(subdirectory): #move all .wav files into a subfolder named wav.
    cwd = os.getcwd()
    if not os.path.isdir(subdirectory+'/wav'):
        os.makedirs(subdirectory+'/wav')
    command = 'mv '+cwd+'/'+subdirectory+'/*.wav '+cwd+'/'+subdirectory+'/wav/'
    print command
    subprocess.check_output(['bash','-c', command])
    print 'wav files moved'
    print 'current directory: ', os.getcwd()

if __name__ == "__main__":
    keyword = sys.argv[1]
    currentPath = os.getcwd() + '/data/xeno-canto/' + keyword
    rename(currentPath, keyword + '_fs')
    convertToWav(currentPath)
    movewavfiles('data/xeno-canto/' + keyword)
