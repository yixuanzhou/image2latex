#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  im2latex_utils.py
#  Collection of tools to help with im2latex  
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
import random 
import argparse

# regexp used to tokenize formula
#   Pattern /[$-/:-?{-~!"^_`\[\]]/ was taken from:
#       http://stackoverflow.com/questions/8359566/regex-to-match-symbols
TOKENIZE_PATTERN = re.compile("(\\\\[a-zA-Z]+)|"+ # \[command name]
                              #"(\{\w+?\})|"+ # {[text-here]} Check if this is needed
                              "((\\\\)*[$-/:-?{-~!\"^_`\[\]])|"+ # math symbols
                              "(\w)|"+ # single letters or other chars
                              "(\\\\)") # \ characters

# regexps for removing "invisible" parts
# First item is regexp for searching, second is string/func used to replace
INVISIBLE_PATTERNS = [[re.compile("(\\\\label{.*?})"), ""],
                      [re.compile("(\$)"), ""],
                      [re.compile("(\\\>)"), ""],
                      [re.compile("(\\\~)"), ""],
                     ]

# regexps for normalizing
# First item is regexp for searching, second is string/func used to replace
NORMALIZE_PATTERNS = [[re.compile("\{\\\\rm (.*?)\}"), 
                            lambda x: "\\mathrm{"+x.group(1)+"}"],
                      [re.compile("\\\\rm{(.*?)\}"), 
                            lambda x: "\\mathrm{"+x.group(1)+"}"],
                      [re.compile("SSSSSS"), "$"],
                      [re.compile(" S S S S S S"), "$"],
                     ]
                

def tokenize_formula(formula):
    """Returns list of tokens in given formula.
    formula - string containing the LaTeX formula to be tokenized
    Note: Somewhat work-in-progress"""
    # Tokenize
    tokens = re.finditer(TOKENIZE_PATTERN, formula)
    # To list
    tokens = list(map(lambda x: x.group(0), tokens))
    # Clean up
    tokens = [x for x in tokens if x is not None and x != ""]
    return tokens

def remove_invisible(formula):
    """Removes 'invisible' parts of the formula.
    Invisible part of formula is part that doesn't change rendered picture, 
    eg. \label{...} doesn't change the visual output of formula 
    formula -- formula string to be processed 
    Returns processed formula
    Note: Somewhat work-in-progress"""
    for regexp in INVISIBLE_PATTERNS:
        formula = re.sub(regexp[0], regexp[1], formula)
    return formula
    
def normalize_formula(formula):
    """Normalize given formula string.
    Normalisation attempts to eliminate multiple different ways of writing
    same thing. Eg. 'x^2_3' results to same output as 'x_3^2', and normalisation
    would turn all of these to same form
    formula -- formula string to be normalised
    Returns processed formula
    Note: Somewhat work-in-progress"""
    for regexp in NORMALIZE_PATTERNS:
        formula = re.sub(regexp[0], regexp[1], formula)
    return formula

def split_train_validate_test(array, frac=0.8):
    """ Splits given array into train, validation and test sets
    First splits array into train-test sets (frac for train, 1-frac for test),
    then splits train set into train-validation (again, frac for train and
    1-frac for validation)
    array - array to be splitted into three non-overlapping sets
    frac  - Fraction of items to keep in train set in splits
    Returns list of lists [train, validation, test]"""
    idxs = set(range(len(array))) 
    #Take test set
    test_idxs = set(random.sample(idxs, int(len(idxs)*(1.0-frac))))
    idxs = idxs-test_idxs
    
    validate_idxs = set(random.sample(idxs, int(len(idxs)*(1.0-frac))))
    idxs = idxs-validate_idxs
    
    test = [array[i] for i in test_idxs]
    validate = [array[i] for i in validate_idxs]
    train = [array[i] for i in idxs]
    return [train, validate, test]

