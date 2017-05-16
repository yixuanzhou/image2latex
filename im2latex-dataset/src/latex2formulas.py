#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  latex2formulas.py
#  Parses tar files of latex files for formulas
#
#  © Copyright 2016, Anssi "Miffyli" Kanervisto
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

def main(directory):
    latex_tars = glob.glob(directory+"*.tar.gz")
    formulas = []
    ctr = 0
    for filename in latex_tars:
        tar = tarfile.open(filename)
        #List latex files
        files = tar.getnames()
        #Loop over and extract results
        for latex_name in files:
            if not "/" in latex_name: #.getnames() includes directory-only
                continue
            tar.extract(latex_name)
            latex = open(latex_name).read()
            formulas.extend(get_formulas(latex))
            os.remove(latex_name)
        ctr += 1
        print("Done {} of {}".format(ctr, len(latex_tars)))
    formulas = list(set(formulas))
    print("Parsed {} formulas".format(len(formulas)))
    print("Saving formulas...")
    
    with open("formulas.txt", "w") as f:
        f.write("\n".join(formulas))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: latex2formulas tar_directory\n"+    
              "tar_directory should hold .tar files containing latex sources")
    else:
        main(sys.argv[1])

