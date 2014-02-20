#!/usr/bin/env python
import os
import zipfile

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('/data_out/Python.zip', 'w')
    zipdir('data_in/', zipf)
    zipf.close()
