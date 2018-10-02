# autograding
Automatic pre-grading of course submissions.

A simple, flexible toolchain for automatically pre-grading submissions for assignments in computer science courses.

## Features

- simple, modular scripts that can be easily extended and adjusted
- pre-grading solutions using either regular expressions or custom Python functions (which may call external tools)
- relatively robust against bad input
- tools for distributing assignments to graders and for combining the graded submissions again (via CSV files)

## Limitations

- only works with submissions in plain text files (using custom scripts, it is also able to auto-grade further files, such as PDFs)
- make assumptions about the file name structure (i.e., Moodle ID and student's names have to be included in file name of submission)
- makes assumptions about internal structure of submissions
- underdocumented and hackish code

## Contact

`autograding` is used in a few large introductory courses at the University of Regensburg.

Contact [Raphael Wimmer](https://www.uni-regensburg.de/sprache-literatur-kultur/medieninformatik/sekretariat-team/raphael-wimmer/index.html) for any questions (or file an issue on GitHub).

