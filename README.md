# Tracker

A command-line tool to check progress of data collection by The OpenElections Project.

The `openelex-tracker` command generates various files and reports.

The goal is to measure our progress toward generating four file types in each state:

* county-level general election results
* precinct-level general election results
* county-level primary election results
* precinct-level primary election results

Other elections, including office-specific primaries, may also be included where available.

> **See the Technical Background section below for more details.**

Metrics on Github activity, repo creation, etc. are also fair game...

## Install

* Install Python 3.6 
* [Create a Github personal access
  token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)
* Add Github access token to `.bashrc` or `.bash_profile`: `GITHUB_PERSONAL_ACCESS_TOKEN=<TOKEN>` 
* Clone the repo and install:

```
git clone git@github.com:openelections/tracker.git
cd tracker/
# Install the CLI tool into active python 3.6
make install
```

##  Use

```
# List available actions
openelex-tracker --help
```

## Contribute

To contribute code:

### Setup

```
cd /path/to/tracker
echo "PYTHONPATH=$(pwd)" > .env
pip install pipenv
```

### Run tests

```
make test
```

## Technical Background

OpenElections has dozens of data-oriented Github repositories containing minimally processed 
data from source agencies. In some cases, these data files may be hand-keyed.

This "raw" data is stored in its *pre-processed* form on Github in
repositories that follow the below naming conventions:

 >  *openelections-[source|data]-[state-postal]*

For example:

* [openelections-sources-tx](https://github.com/openelections/openelections-data-tx)
* [openelections-data-tx](https://github.com/openelections/openelections-data-tx)

The *-sources-* repos contain data files in their most raw form, such as unconverted image pdfs. 

The *-data-* repos contain data in a *minimally processed* form, such as data files which have been extracted from PDFs but reflect the same field names, data values etc. as the original PDFs.

The files in *-data-* repos serve as the raw input for the OpenEletions data standardiztion pipeline.

The *-sources-* and *-data-* repos organize election result files into year-based directories. These files follow a naming convention based on OpenCivic identifiers.

TK - examples of file names...


