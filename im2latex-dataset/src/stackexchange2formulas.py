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
import html
import xml.etree.ElementTree as ET

PATTERNS = [r"\\begin\{equation\}(.*?)\\end\{equation\}",
            r"\$\$(.*?)\$\$",
            r"\$(.*?)\$",
            r"\\\[(.*?)\\\]",
            r"\\\((.*?)\\\)"]
DIR = ""

#Number of bytes required for formula to be saved
MIN_LENGTH = 20
MAX_LENGTH = 2048

def get_formulas(message_body):
    """ Returns detected formulas from given stackexchange message body
    Returns list of formula strings"""
    ret = []
    # Assume math is only inside <p> tags. Need to check this
    message_body = " ".join(re.findall("<p>(.*?)</p>", message_body, re.DOTALL))
    for pattern in PATTERNS:
        res = re.findall(pattern, message_body, re.DOTALL)
        #Remove short ones
        res = [x.strip().replace("\n","").replace("\r","") for x in res if 
               MAX_LENGTH > len(x.strip()) > MIN_LENGTH]
        ret.extend(res)
    return ret

def get_bodies(stackexchange_data):
    """ Parses given XML stackexchange_data into set of message bodies
    Returns list of strings (message bodies"""
    xml = ET.fromstring(stackexchange_data)
    bodies = []
    for child in xml.getchildren():
        body = child.get("Body")
        if body is not None:
            body = html.unescape(body)
            # Check if ASCII so we won't get any fancy characters
            # Code from: stackoverflow.com/questions/196345
            if all(ord(c) < 128 for c in body):
                bodies.append(body)
    return bodies
            
def main(directory):
    # support .tar and .tar.gz
    stackexchange_tars = glob.glob(directory+"*.tar")
    stackexchange_tars.extend(glob.glob(directory+"*.tar.gz"))
    formulas = []
    ctr = 0
    for filename in stackexchange_tars:
        tar = tarfile.open(filename)
        #List latex files
        files = tar.getnames()
        #Loop over and extract results
        for xml_name in files:
            if xml_name == "/": #.getnames() includes directory-only
                continue
            xml_file = tar.extractfile(xml_name)
            stackexchange_data = xml_file.read().decode()
            message_bodies = get_bodies(stackexchange_data)
            for body in message_bodies:
                formulas.extend(get_formulas(body))
        ctr += 1
        print("Done {} of {}".format(ctr, len(stackexchange_tars)))
        tar.close()
    formulas = list(set(formulas))
    print("Parsed {} formulas".format(len(formulas)))
    print("Saving formulas...")
    
    with open("formulas.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(formulas))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: stackexchange2formulas tar_directory\n"+    
              "tar_directory should hold .tar files containing XML files from"+
              " StackExchange")
    else:
        main(sys.argv[1])

