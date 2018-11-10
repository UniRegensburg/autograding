#!/usr/bin/env python3

import sys
import os
import re
from collections import deque
from csv import DictReader, DictWriter, Sniffer

def combine_assignments(csv_file_list):
    FIELD_NAMES = "ID,Bewertung,Skala,Zuletzt geändert (Bewertung),Feedback als Kommentar".split(",")
    FEEDBACK_COLUMN = "Feedback als Kommentar"
    SKALA = """nicht ausreichend
ok
gut"""
    REMOVE_FIELDS = "Punkte,Name,Korrektor".split(",")

    writer = DictWriter(sys.stdout, FIELD_NAMES)
    writer.writeheader()
    for csv_file in csv_file_list:
        with open(csv_file, "r") as fd:
            firstchar = fd.read(1)
            if firstchar in ["\ufeff", "\ufffe"]:  # BOM
                pass
            else:
                fd.seek(0)
            # dialect = Sniffer().sniff(fd.read(1024))
            # fd.seek(0)
            # print(">>> " + str(dialect.delimiter))
            # reader = DictReader(fd, dialect=dialect)
            reader = DictReader(fd)
            for row in reader:
                # try:
                    row["Skala"] = SKALA
                    for remove_field in REMOVE_FIELDS:
                        row.pop(remove_field)
                    feedback = row[FEEDBACK_COLUMN]
                    new_feedback = []
                    for line in feedback.splitlines():
                        line = line.replace("<", "&lt;").replace(">", "&gt;")
                        line = re.sub(r'[^\x00-\xFF]+', '(U)', line)  # remove Unicode chars - Moodle doesn't like them
                        line = "<p>" + line + "</p>"
                        new_feedback.append(line)
                    new_feedback = " \n".join(new_feedback)  # make it a string
                    row[FEEDBACK_COLUMN] = new_feedback
                    writer.writerow(row)
                # except Error e:
                #    print(">>> " + str(row) + str(e), file=sys.stderr)
    # done
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: %s <file1.csv> [...]" % sys.argv[0])
        sys.exit(-1)
    # else
    csv_files = sys.argv[1:]
    combine_assignments(csv_files)

