#import numpy as np
import os
import shutil


def createTimelaps(name, date = None, path = None):
    staticPath = "output"
    if date:
        path = 'archive/' + name + '/' + date
    elif path == None:
        print("Error-Timelapse-missing args for folder")
        return -1

    if not os.path.exists(path):
        print("Error-Timelapse-can't finde folder", path)
        return -2

    ## Check if folder exists and is not empty
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            print("Error-Timelapse-Empty directory", path)
            return -3

    #print('creating writer')
    #videoSize = (
    #    img_array[0].shape[1],
    #    img_array[0].shape[0]
    #)
    #writer = cv2.VideoWriter( path + '/' + name + '.mp4', cv2.VideoWriter_fourcc(*"mp4v"), 10, videoSize)
    #print('writer created')
    #print()

        
    print('creating video')
    
    if os.path.exists(path + "/" + name + ".mp4"):
        print("video allready exists")
        os.remove(path + "/" + name + ".mp4")
    imgWidht = 2304
    imgHeight = 864    
    os.system('ffmpeg -hide_banner -loglevel error -stats -framerate 10 -pattern_type glob -i "' + path + '/*.jpg" -s:v ' + str(imgWidht) + 'x' + str(imgHeight) + ' -c:v libx264 -crf 17 -pix_fmt yuv420p ' + path + '/' + name + '.mp4')
    
    shutil.copyfile(path + "/" + name + ".mp4", staticPath + "/" + name + ".mp4")
    print('video created')
    print()

    try:
        shutil.make_archive(path, 'zip', path)
        print('zip created')
    except:
        print('Error while creating .zip')

    try:
        shutil.rmtree(path)
        print('folder cleared')
    except:
        print('Error while removing folder')
    

if __name__ == "__main__":
    createTimelaps("kantine", path="timelapse/kantine/20230828")