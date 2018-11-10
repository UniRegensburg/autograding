#!/usr/bin/env python3
# -- coding: utf-8 --

# (c) 2011-2018 Raphael Wimmer <raphael.wimmer@ur.de>
# Licensed under the MIT license

import sys
import re
import os
import codecs
import magic
import glob
from types import *
import builtins


'''The working directory from which this script is started should contain the following files:
    - u01_solution.txt (a solution file)
    - custom.py (for custom scripts)
    - abgaben/Mustermann_Max_1234_u01.txt (etc.)

'''
PRINT_HTML = False

CUR_DIR = os.getcwd() 
sys.path.insert(0, CUR_DIR)
TEMPLATE = glob.glob(os.path.join(CUR_DIR, "./u*_solution.txt"))[0]

try:
    from custom import *
except ModuleNotFoundError:
    pass

# global info available for all functions (hack that makes it easier for custom.py)
builtins.firstname = ""
builtins.lastname = ""
builtins.matrikel_nummer = ""
builtins.uid = ""
builtins.feedback_list = []

def err(line):
    print("# >>> " + line)

builtins.err = err

builtins.max_points = 0
builtins.format_correct_points = 5 # changed by script 
builtins.bonus_points = 0


def calc_max_points(solution):
    points = 0
    for line in solution.split("\n"):
        if "#" in line:
            points += int(line.split("#")[-1].strip())
    return points


def grade_assignment(assignment, grading_template):
    # order important here, because matrikel_nummer is set by both parse_solution() calls - but only the Matrikelnummer from the solution is what we want to remember
    c_sols = parse_solution(grading_template)
    sols = parse_solution(assignment)
    points = 0
    for c_task in c_sols:
        solution_submitted = False
        for task in sols: # find solution in list
            if ((c_task[0] == task[0]) and (c_task[1] == task[1])):
                solution_submitted = True
                cur_sol = task[2]
        print("# " +c_task[0] + c_task[1] + ": ", end='')
        if not solution_submitted:
            feedback_list.append(c_task[0] + c_task[1] + ": fehlt!")
            print("#fehlt")
        else: 
            cur_c_sol, cur_c_points = c_task[2].split("#")
            cur_c_sol = cur_c_sol.strip()
            cur_c_points = int(cur_c_points.strip())
            cur_points, cur_feedback = check_solution(cur_sol, cur_c_sol, cur_c_points)
            print("# " + cur_sol + " " + cur_feedback + " (" + str(cur_points) + "/" + str(cur_c_points) + " Punkten)")
            feedback_list.append(c_task[0] + c_task[1] + ": (" + cur_sol + ") " + cur_feedback)
            points += cur_points
    return points

def check_solution(solution, correct_solution, correct_points):
    # find out type of correct_solution (regex or function)
    if len(solution.strip()) == 0:
        return (0, "fehlt!") # should already have been caught by grade_assignment
    if correct_solution.startswith("/"): # regex handling
        if re.match(correct_solution.strip("/"), solution, flags=re.IGNORECASE) != None:
            return (correct_points, "ist korrekt!")
        else:
            return (0, "ist falsch!")
    elif correct_solution.startswith("{") and correct_solution.endswith("}"):
        # TODO: handle dicts
        err("Dictionary check not implemented yet")
    elif correct_solution.endswith("()"):
        check_func = correct_solution.strip("()")
        return (eval(check_func + "(\"" + solution.replace('"',"'") + "\")"))
    else:
        err("OOPS")
        return (0, "")


# both for grading template and actual solution by student
def parse_solution(text):
    global format_correct_points
    tasks = []
    cur_task = None
    cur_subtask = None
    solution =""
    builtins.matrikel_nummer = text.splitlines()[0]
    for line in text.splitlines()[1:]:
        line = line.strip(" \t")
        if len(line) == 0:
            continue
        elif line.startswith("Aufgabe"):
            cur_task = line.strip(": ")
            for (t,st,s) in tasks:
                if t == cur_task:
                    err("Achtung, mehrere Lösungen für %s - manuell überprüfen. Punktabzug!" % (cur_task))
                    feedback_list.append("Punktabzug - mehrere Lösungen für %s" % (cur_task))
                    builtins.format_correct_points -= 1
            cur_subtask = ""
            solution = ""
        elif re.match("^[a-z]\)", line) != None:
            cur_subtask = line[0:2]
            solution = line[2:].strip() # strip because of potential  whitespace between "a)" and solution
        else:
            solution += (line + " ")
        if solution != "":
            if cur_task is not None:
                tasks.append((cur_task,cur_subtask,solution))
            else:
                err("Punktabzug - Lösung ohne zugehörige Aufgabe: " + solution)
                feedback_list.append("Punktabzug - Lösung ohne zugehörige Aufgabe: " + solution)
                builtins.format_correct_points -= 1

    return tasks

def load_and_clean(textfile):
    warned_about_lt_gt_signs = False
    real_filename=os.path.basename(textfile)
    names = re.findall(r"[a-zA-ZäöüßÄÖÜ]+", real_filename)[0:-2]
    builtins.lastname = names[0]
    builtins.firstname = names[1]
    builtins.uid = re.findall(r"[0-9]{7}", real_filename)[0]
    print("#")
    print("#############################################################################")
    print("# %s, %s (%s) " % (lastname, firstname, uid))
    print("#############################################################################")


    format_correct_points = 5
    mag = magic.open(magic.MAGIC_MIME_ENCODING)
    mag.load()
    orig_filename = textfile.split("_")[3:]
    orig_filename = "_".join(orig_filename)
    if re.match("u[0-9]{2}", orig_filename) == None:
        feedback_list.append("Punktabzug für falschen Datei-Namen: " + orig_filename)
        print("# Punktabzug für falschen Datei-Namen: " + orig_filename + ".txt")
        format_correct_points -= 2
    encoding = mag.file(textfile)
    if not encoding in ["utf-8", "us-ascii"]:
        feedback_list.append("Punktabzug für falsches Datei-Encoding: " + encoding )
        print("# Punktabzug für falsches Datei-Encoding: " + encoding )
        format_correct_points -= 2
    print("# " + encoding)
    try:
        codecs.lookup(encoding) # fails if encoding not decodeable
    except LookupError:
        err("Encoding kann nicht konvertiert werden: " + encoding)
        return ""
    text = codecs.open(textfile, 'r', encoding).read()
    # strip BOM
    text = text.strip("\ufeff")
    # convert all newline variants to "\n"
    text = text.replace("\r\n","\n").replace("\r","\n")
    # convert non-breaking whitespace to regular whitespace
    text = text.replace("\xa0"," ")
    for line in text.splitlines():
        if "<" in line[0:4] and line.strip().endswith(">"):
            if not warned_about_lt_gt_signs:
                feedback_list.append("Punktabzug - Lösungen in spitzen Klammern :(  ")
                print("# Punktabzug - Lösung(en) in spitzen Klammern :(  ")
                warned_about_lt_gt_signs = True
                format_correct_points -= 1


    print("# Punkte für korrektes Abgabeformat: " + str(format_correct_points) + "/5 Punkten")
    return text, format_correct_points


def calc_score(points, format_correct_points, max_points):
    if format_correct_points < 0:
        format_correct_points = 0
    
    comments = [
          (1.0, "Perfekt! Alles richtig!", "gut"),
          (0.8, "Sehr gut! Fast alles richtig!", "gut"),
          (0.7, "Gut!", "gut"),
          (0.6, "Ok.","ok"),
          (0.5, "Gerade noch ausreichend!","ok"),
          (0.0, "Leider nicht ausreichend!","nicht ausreichend")
          ]
    score = float(points + format_correct_points + bonus_points) / max_points
    print("# ==> Gesamtpunktzahl: " + str(points+format_correct_points+bonus_points) + "/" + str(max_points))
    for comment in comments:
        if score >= comment[0]:
            feedback_list.insert(0,comment[1])
            return comment[2]
    return

def print_score_steps(max_points):
    comments = [
	(1.0, "Perfekt! Alles richtig!", "gut"),
	(0.8, "Sehr gut! Fast alles richtig!", "gut"),
	(0.7, "Gut!", "gut"),
	(0.6, "Ok.","ok"),
	(0.5, "Gerade noch ausreichend!","ok"),
	(0.0, "Leider nicht ausreichend!","nicht ausreichend")
	]
    for percentage, text, grade in comments:
        print("bis %02d Punkte: %s (%s)" % (int(percentage*max_points), text, grade))


# main

correct_solution = open(TEMPLATE, "r").read()

# needs to be first because "format_correct_points" changes in load_and_clean().
max_points = calc_max_points(correct_solution) + format_correct_points + bonus_points

# just print out the score steps
if sys.argv[1] == "--scores":
   print_score_steps(max_points)
   sys.exit(0)

sol,format_correct_points = load_and_clean(sys.argv[1])
points = grade_assignment(sol, correct_solution)
grade = calc_score(points, format_correct_points, max_points)

# finally
# print ("\nFEEDBACK\n========\n")
csv_start = 'Teilnehmer/in%s,"%s",%d,"%s","' % (uid, lastname+", "+firstname, points+format_correct_points, grade)
csv_end = '"'
print(csv_start)
for line in feedback_list:
    line = line.replace('"',"'") # messes with CSV!
    if PRINT_HTML:
        line = line.replace("<", "&lt;").replace(">", "&gt;").replace('"',"'")
        line = "<p> " + line + " </p>"
    print(line)
print(csv_end)

