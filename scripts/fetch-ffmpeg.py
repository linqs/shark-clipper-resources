#!/usr/bin/env python3

import argparse
import gzip
import os
import shutil
import sys
import tarfile
import urllib.request
import zipfile

import util

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, '..'))
OUT_DIR = os.path.join(ROOT_DIR, 'ffmpeg')

LINUX_TARGET = 'https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz'
MAC_TARGET_FFMPEG = 'https://evermeet.cx/ffmpeg/ffmpeg-7.0.1.zip'
MAC_TARGET_FFPROBE = 'https://evermeet.cx/ffmpeg/ffprobe-7.0.1.zip'
WIN_TARGET = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'

def _fetch_linux():
    print("Fetching Linux FFmpeg Binaries")

    temp_dir = util.get_temp_path(prefix = 'shark-clipper-fetch-ffmpeg-')

    out_dir = os.path.join(OUT_DIR, 'linux')
    os.makedirs(out_dir, exist_ok = True)

    response = urllib.request.urlopen(LINUX_TARGET)

    archive_path = os.path.join(temp_dir, 'ffmpeg-release-amd64-static.tar.xz')
    with open(archive_path, 'wb') as file:
        file.write(response.read())

    extract_dir = os.path.join(temp_dir, 'extract')
    with tarfile.open(archive_path) as archive:
        archive.extractall(path = extract_dir, filter = 'data')

    versioned_dirname = os.listdir(extract_dir)[0]

    for name in ['ffmpeg', 'ffprobe']:
        in_path = os.path.join(extract_dir, versioned_dirname, name)
        out_path = os.path.join(out_dir, name)

        _gzip(in_path, out_path)

    return 0

def _fetch_mac():
    print("Fetching Mac FFmpeg Binaries")

    temp_dir = util.get_temp_path(prefix = 'shark-clipper-fetch-ffmpeg-')
    extract_dir = os.path.join(temp_dir, 'extract')

    out_dir = os.path.join(OUT_DIR, 'mac')
    os.makedirs(out_dir, exist_ok = True)

    for (name, target) in [('ffmpeg', MAC_TARGET_FFMPEG), ('ffprobe', MAC_TARGET_FFPROBE)]:
        response = urllib.request.urlopen(target)

        archive_path = os.path.join(temp_dir, name + '.zip')
        with open(archive_path, 'wb') as file:
            file.write(response.read())

        with zipfile.ZipFile(archive_path, 'r') as archive:
            archive.extractall(extract_dir)

        in_path = os.path.join(extract_dir, name)
        out_path = os.path.join(out_dir, name)

        _gzip(in_path, out_path)

    return 0

def _fetch_windows():
    print("Fetching Windows FFmpeg Binaries")

    temp_dir = util.get_temp_path(prefix = 'shark-clipper-fetch-ffmpeg-')

    out_dir = os.path.join(OUT_DIR, 'windows')
    os.makedirs(out_dir, exist_ok = True)

    response = urllib.request.urlopen(WIN_TARGET)

    archive_path = os.path.join(temp_dir, 'ffmpeg-master-latest-win64-gpl.zip')
    with open(archive_path, 'wb') as file:
        file.write(response.read())

    extract_dir = os.path.join(temp_dir, 'extract')
    with zipfile.ZipFile(archive_path, 'r') as archive:
        archive.extractall(extract_dir)

    versioned_dirname = os.listdir(extract_dir)[0]

    for name in ['ffmpeg', 'ffprobe']:
        in_path = os.path.join(extract_dir, versioned_dirname, 'bin', name + '.exe')
        out_path = os.path.join(out_dir, name)

        _gzip(in_path, out_path)

    return 0

def _gzip(source, dest, ensure_ext = True):
    if (ensure_ext and (not dest.endswith('.gz'))):
        dest += '.gz'

    with open(source, 'rb') as in_file:
        with gzip.open(dest, 'wb') as out_file:
            shutil.copyfileobj(in_file, out_file)

def fetch():
    _fetch_mac()
    _fetch_linux()
    _fetch_windows()

    return 0

def main():
    args = _get_parser().parse_args()
    return fetch()

def _get_parser():
    parser = argparse.ArgumentParser(description = "Fetch all FFmpeg binaries.")
    return parser

if __name__ == '__main__':
    sys.exit(main())
