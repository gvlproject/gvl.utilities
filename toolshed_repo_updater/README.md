## toolshed_repo_updater.py

This script will take in the yaml file of toolshed tools to be installed and checks their revisions. It prints --> stdout a tab delimited list of tools that have newer revisions in the appropriate toolshed. It also outputs a yaml file of the tools to be installed with all of the revisions updated.

Example:

      $ cd gvl.utilities/toolshed_repo_updater
      $ python toolshed_repo_updater.py -i input.yaml -o output.yaml

Usage:

      usage: toolshed_repo_updater.py [-h] [-v] -i INPUT -o OUTPUT

      optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Verbose output to STDERR
      
      required arguments:
      -i INPUT, --input INPUT
                        Input file name
      -o OUTPUT, --output OUTPUT
                        Output file name
