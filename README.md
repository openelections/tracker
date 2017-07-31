# Tracker
### Progress tracker for OpenElections work

The files in this repository show the extent of OpenElections' work on election results by state per election year. There is one file for each election year, with columns for each state and the current status of work for four stages:

* county-level general election results
* precinct-level general election results
* county-level primary election results
* precinct-level primary election results

Other elections, including office-specific primaries and special elections, may be added but are optional.

The stages of work are defined as followed:

* working - work is in progress for that state and election
* CSV - a complete set of converted CSV files exist in openelections-data-{abbrev} repositories
* Baked raw - a complete set of raw published results files exist in openelections-results-{abbrev} repositories

A blank value means that work on that state and results level has not begun.
