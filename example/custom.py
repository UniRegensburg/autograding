#!/usr/bin/env python3
# -- coding: utf-8 --

import sys
import re
import os
import codecs
import magic
from types import *

# custom
def check_substantive(string):
    tests  = [ ("Eva kauft ein Buch.", ["ein Buch"]),
               ("Hier: der Buch das Hut", ["der Buch", "das Hut"]),
               ("kein Hut Buch ein", [])
    ]
    return grade_regex(string, tests)

def check_exclamation_mark(string):
    tests  = [ ("Eva kauft ein Buch!", ["Eva kauft ein Buch!"]),
               ("Das Buch! Der Hut!", ["Das Buch!", "Der Hut!"]),
               ("Kein Hut? Ein Buch.", [])
    ]
    return grade_regex(string, tests)

def check_hex(string):
    tests  = [ ("Zahl: 0xaf", ["0xaf"]),
               ("Zahlen: 0x3d 0xAB 0xgg", ["0x3d", "0xAB"]),
               ("Zahl: 0xx0 12", [])
    ]
    return grade_regex(string, tests)

def check_defd(string):
    tests  = [ ("defed", ["defed"]),
               ("dd", ["dd"]),
               ("de", [])
    ]
    return grade_regex(string, tests)

def grade_regex(string, tests):
    feedback = ""
    points = 0
    try:
        for s_m in tests:
            p, f = check_regex(string, s_m[0], s_m[1])
            points += p
            feedback = feedback + " - " + f
    except: 
        return (0, "konnte nicht automatisch geprüft werden.")
    return (points, feedback)



def check_regex(regex, string_to_test, expected_matches):
    #print("#>>>>> %r " % (regex))
    find_global = False
    flags = 0
    if not regex.endswith("/"):
        if "i" in regex[regex.rfind("/")+1:]:
            flags |= re.IGNORECASE 
        if "m" in regex[regex.rfind("/")+1:]:
            flags |= re.MULTILINE
        if "g" in regex[regex.rfind("/")+1:]:
            find_global = True
    regex = regex.strip(" gim").strip("/").replace("(", "(?:").replace("(?:?:", "(?:")
    #print("#>>>> %r " % (regex))
    try:
        matches = re.findall(regex, string_to_test) 
    except SyntaxError:
        return (0, "invalider regulärer Ausdruck")
    if (not find_global) and len(matches) > 0:
        matches = [matches[0]]
    #print("#>>>> Matches: " + str(matches))
    matches = map(lambda x: x.strip(), matches) # Leerzeichen wegstrippen, d.h. kulanter bewerten
    matches = set(matches)
    expected_matches = set(expected_matches)
    if matches == expected_matches:
        return (1, "korrekt für: '%s'" % (string_to_test))
    else:
        return (0, "findet falsche Treffer für: '%s': %s" % (string_to_test, ", ".join(matches)))

# end custom
