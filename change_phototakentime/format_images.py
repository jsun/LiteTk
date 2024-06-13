import os
import sys
import datetime
import subprocess
import re
import glob
import pytz
import tqdm
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
import json




def get_exif(fpath):
    if os.path.splitext(fpath)[1].lower() not in ['.png', '.jpg', '.jpeg']:
        return {}
    im = Image.open(fpath)
    exif = None
    try:
        exif = im._getexif()
    except AttributeError:
        return {}
    if exif is None:
        return {}
    exif_table = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        exif_table[tag] = value
    return exif_table





def get_yyyymm(fpath):
    dt = None
    
    # find datetime from JSON (Google Photos format)
    if os.path.exists(fpath + '.json'):
        meta = {}
        with open(fpath + '.json') as infh:
            meta = json.load(infh)

        if 'photoTakenTime' in meta:
            dt = datetime.datetime.strptime(meta['photoTakenTime']['formatted'],
                                            '%Y/%m/%d %H:%M:%S %Z').replace(tzinfo=pytz.timezone('Japan'))
    # find datetime from EXIF
    if dt is None:
        exif = get_exif(fpath)
        if 'DateTimeOriginal' in exif:
            dt = datetime.datetime.strptime(exif['DateTimeOriginal'],
                                            '%Y:%m:%d %H:%M:%S')
    
    # find datetime from metadata if file is movie
    if os.path.splitext(fpath)[1] == '.mp4' and dt is None:
            cmd_outputs = subprocess.run(['ffmpeg', '-i', fpath], capture_output=True, text=True)
            for _ in cmd_outputs.stderr.splitlines():
                m = re.match(r'\s*creation_time\s*:\s*(\S+)Z', _)
                if m:
                    dt = datetime.datetime.fromisoformat(m.group(1)) + datetime.timedelta(hours=9)

    return dt




def valid_image(fpath):
    v = True
    if not os.path.isfile(fpath):
        v = False
    if os.path.splitext(fpath)[1].lower() not in ['.jpg', '.jpeg', '.mp4']:
        v = False
    return v



def sort_images(from_dpath, to_dpath):

    for batch_dpath in tqdm.tqdm(glob.glob(os.path.join(from_dpath, '*'))):
        for fpath in tqdm.tqdm(glob.glob(os.path.join(from_dpath, '**'), recursive=True), leave=False, desc=batch_dpath):
            if valid_image(fpath) is False:
                continue
            
            # get shooting time
            shooting_dt = get_yyyymm(fpath)
            if shooting_dt is not None:
                os.utime(fpath, (shooting_dt.timestamp(), shooting_dt.timestamp()))

                # move files
                to_dpath_ = os.path.join(to_dpath, shooting_dt.strftime('%Y/%m'))
                if not os.path.exists(to_dpath_):
                    os.makedirs(to_dpath_, exist_ok=True)
                to_fname = os.path.basename(fpath)
                to_fpath = os.path.join(to_dpath_, to_fname)
                print([fpath, to_fpath])
                shutil.move(fpath, to_fpath)


if __name__ == '__main__':
    d_from = sys.argv[1]
    d_to = sys.argv[2]
    sort_images(d_from, d_to)



