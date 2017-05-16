#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arxiv2formulas.py
#  Parses arxiv tar files of source files for latex formulas
#
#  © Copyright 2017, mitar (https://github.com/mitar)
#                    Anssi "Miffyli" Kanervisto
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  
import re
import tarfile
import os
import glob
import sys
import codecs

PATTERNS = [r"\\begin\{equation\}(.*?)\\end\{equation\}",
            r"\$\$(.*?)\$\$",
            r"\$(.*?)\$",
            r"\\\[(.*?)\\\]",
            r"\\\((.*?)\\\)"]
DIR = ""

#Number of bytes required for formula to be saved
MIN_LENGTH = 40
MAX_LENGTH = 1024

def get_formulas(latex):
    """ Returns detected latex formulas from given latex string
    Returns list of formula strings"""
    ret = []
    for pattern in PATTERNS:
        res = re.findall(pattern, latex, re.DOTALL)
        #Remove short ones
        res = [x.strip().replace("\n","").replace("\r","") for x in res if 
               MAX_LENGTH > len(x.strip()) > MIN_LENGTH]
        ret.extend(res)
    return ret

def process_file(tar, file_name):
    file_basename, file_extension = os.path.splitext(file_name)
    if file_extension == '.pdf':
        return []
    elif file_extension == '.tar':
        return process_tar(tar.extractfile(file_name))
    elif file_extension == '.gz':
        return process_tar(tar.extractfile(file_name))
    elif file_extension == '.tex':
        try:
            file_content = codecs.decode(tar.extractfile(file_name).read(), 'ascii')
        except:
            return []
        return get_formulas(file_content)
    else:
        return []

def process_tar(file):
    formulas = []
    tar = None
    try:
        tar = tarfile.open(fileobj=file, mode='r:*')
    except:
        return []
    files = tar.getnames()
    for file_name in files:
        formulas.extend(process_file(tar, file_name))
    return formulas

def main(directory):
    arxiv_tars = glob.glob(directory+"*.tar")
    arxiv_tars.extend(glob.glob(directory+"*.tar.gz"))
    formulas = []
    ctr = 0
    for filename in arxiv_tars:
        with open(filename, "rb") as tar_file:
            processed_formulas = process_tar(tar_file)
            if len(processed_formulas) == 0:
                print("File %s returned 0 formulas. Invalid file?" % filename)
            else:
                formulas.extend(processed_formulas)
        ctr += 1
        print("Done {} of {}".format(ctr, len(arxiv_tars)))
    formulas = list(set(formulas))
    print("Parsed {} formulas".format(len(formulas)))
    print("Saving formulas...")
    
    with codecs.open("formulas.txt", mode="w", encoding="ascii") as f:
        for formula in formulas:
            try:
                f.write("{}\n".format(formula))
            except:
                print("error", formula)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: arxiv2formulas tar_directory\n"+    
              "tar_directory should hold .tar files containing arxiv sources")
    else:
        main(sys.argv[1])

