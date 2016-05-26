## toolshed_repo_updater.py

This script will take in the yaml file of toolshed tools to be installed and checks their revisions. It prints --> stdout a tab delimited list of tools that have newer revisions in the appropriate toolshed. It also outputs a yaml file of the tools to be installed with all of the revisions updated.

Example:

      $ cd gvl.utilities/toolshed_repo_updater
      $ python toolshed_repo_updater.py -i input.yaml -o output.yaml

Usage:

      usage: toolshed_repo_updater.py [-h] [-v] -i INPUT [-s SED_FILE] -o OUTPUT

      optional arguments:
        -h, --help            show this help message and exit
        -v, --verbose         Verbose output to STDERR
        -i INPUT, --input INPUT
                              Input file name
        -s SED_FILE, --sed-file SED_FILE
                              Output sed script file
        -o OUTPUT, --output OUTPUT
                              Output file name

If you want to keep comments from your input yaml file, you can choose to output
a sed script file which you can use with your orignal input yaml file like so:

```bash
python toolshed_repo_updater.py \
    -i test_data/test_input.yml \
    -o test_data/test_output.yml \
    -s test_data/revisions.sed

sed -f test_data/revisions.sed \
    test_data/test_input.yml \
    > test_data/test_output_keep_comments.yml
```
