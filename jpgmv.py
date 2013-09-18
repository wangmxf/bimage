# -*- coding: Windows-1251 -*-
'''
manage image file according to EXIF-date using PIL

'''

import Image

import os
import re
import sys
import time
import shutil
import random

def extract_jpeg_exif_time(jpegfn):
    if not os.path.isfile(jpegfn):
        return None
    try:
        im = Image.open(jpegfn)
        if hasattr(im, '_getexif'):
            exifdata = im._getexif()
            ctime = exifdata[0x9003]
            #print ctime
            return ctime
    except:
        _type, value, traceback = sys.exc_info()
        print "Error:\n%r", value

    return None

def get_exif_prefix(jpegfn):
    ctime = extract_jpeg_exif_time(jpegfn)
    if ctime is None:
        return None
    ctime = ctime.replace(':', '')
    ctime = re.sub('[^\d]+', '', ctime)
    return ctime

def move_jpeg_file(src, dst):
    if not os.path.isfile(src):
        return 0
    if not os.path.isdir(dst):
        return 0
    ext = os.path.splitext(src)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.jfif']:
        return 0
    path, base = os.path.split(src)
    print base # status
    prefix = get_exif_prefix(src)
    if prefix is None:
        return 0
    ystr = prefix[0:4]
    ypath = os.path.join(dst, ystr)
    if not os.path.exists(ypath):
        os.mkdir(ypath)

    new_namex = prefix[4:14]
    new_name = new_namex +'00'+ ext
    new_full_name = os.path.join(ypath, new_name)

    while os.path.exists(new_full_name):
        npath, nbase = os.path.split(new_full_name)
        #fname, ext = os.path.splitext(nbase)
        fname = new_namex + str(random.randrange(10,99)) + ext
        new_full_name = os.path.join(npath, fname)

    try:
        shutil.copyfile(src, new_full_name)

    except:
        print 'ERROR copy %s --> %s' % (src, new_full_name)
        return 0

    return 1

def move_jpeg_files_in_dir(src, dst):
    names = os.listdir(src)
    count=0
    for onename in names:
        if os.path.isdir(os.path.join(src,onename)):
            move_jpeg_files_in_dir(os.path.join(src, onename), dst)
        else:
            file_path = os.path.join(src, onename)
            count += move_jpeg_file(file_path, dst)
    return count


if __name__=='__main__':
    try:
        src = sys.argv[1]
        dst = sys.argv[2]
    except IndexError:
        sys.exit(1)

    if not os.path.exists(dst):
        try:
            os.mkdir(dst)
        except:
            print "can not create %s" % (dst)

    if os.path.isfile(src):
        move_jpeg_file(src, dst)
    elif os.path.isdir(src):
        count = move_jpeg_files_in_dir(src,dst)
    else:
        print 'ERROR: path not found: %s' % path
