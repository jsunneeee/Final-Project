# CSE 163 Project Part 2 - EDA code

The project analyzes documented AI and search crawler identities. It does
not measure actual website blocking rates.

The existing report figures were generated using an offline transcription of
the ten records described in the source README. Before submitting, run the
scripts on the original CSV and verify whether the resulting counts and
figures match the draft report.

From the project folder:

python eda.py
python test_eda.py
flake8 eda.py test_eda.py

The first command prints dataset dimensions, missingness, and counts for
every column, then saves two plots under `figures`. The second runs four
assert-based tests.
