#!/usr/bin/env python3

import sys
import os
from collections import deque
from csv import DictReader, DictWriter

def distribute_assignments(csv_file, graders_list):
    FEEDBACK_COLUMN = "Feedback als Kommentar"
    GRADER_COLUMN = "Korrektor"
    graders = deque(graders_list) # deque allows rotating a list
    with open(csv_file, "r") as fd:
        reader = DictReader(fd)
        fieldnames = reader.fieldnames
        if not GRADER_COLUMN in fieldnames:
            fieldnames.append(GRADER_COLUMN)
        writers = {}
        for grader in graders:
            filename, file_extension = os.path.splitext(csv_file)
            grader_filename = filename + "_" + grader + file_extension
            grader_fd = open(grader_filename, "w")
            writer = DictWriter(grader_fd, fieldnames)
            writer.writeheader()
            writers[grader] = writer
        for row in reader:
            cur_grader = graders[0]
            row[GRADER_COLUMN] = cur_grader
            if row[FEEDBACK_COLUMN] is None:
                print("FEHLENDE Korrektur: %s", row['Name'])
            row[FEEDBACK_COLUMN] += "\nBewertung/Anmerkungen: %s" % cur_grader 
            print("Assigning %s to %s" % (row['Name'],  cur_grader))
            writers[cur_grader].writerow(row)
            graders.rotate(-1)
        # done
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: %s <file.csv> <RW [FD] [MN] ...>" % sys.argv[0])
        sys.exit(-1)
    # else
    csv_file = sys.argv[1]
    graders = sys.argv[2:]
    distribute_assignments(csv_file, graders)

