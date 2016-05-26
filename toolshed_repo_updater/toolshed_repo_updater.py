#!/usr/bin/env python

################################################################################
#
#   toolshed_repo_updater.py
#
#   A script to take in a toolshed tool yaml file (from the
#   ansible-galaxy-tools scripts), check their revisions against the appropriate
#   toolshed, report any tools that have been updated and write out a new yaml
#   file.
#
#   @Author: Simon Gladman, 2016
#
#   TO DO:  1.  Set the toolshed to query be determined by the toolshed key in
#               the yaml objects
#
################################################################################

#Imports
from bioblend import toolshed
import time
import yaml
import argparse


#Toolshed variables. (ATM the script is only configured for the main and test toolshed.)
ts = toolshed.ToolShedInstance(url='https://toolshed.g2.bx.psu.edu')
tts = toolshed.ToolShedInstance(url='https://testtoolshed.g2.bx.psu.edu')

#Commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument('-v','--verbose', help='Verbose output to STDERR', default=False, required=False, action="store_true")
parser.add_argument('-i', '--input', help="Input file name", required=True)
parser.add_argument('-s', '--sed-file', help="Output sed script file", required=False)
parser.add_argument('-o','--output', help='Output file name', required=True)

args = parser.parse_args()

#Read the input yaml file
stream=open(args.input, 'r')
tools = yaml.load_all(stream)
whole_yaml=tools.next()

if args.verbose:
    print whole_yaml

tool_list=whole_yaml['tools']

#Loop through the tools and check their versions using bioblend's toolshed get_ordered_installable_revisions method
print("Tool\tOwner\tCurrent\tLatest")
counter = 0
sed_output = []
for item in tool_list:

    old_version=item.get('revision', 'unknown')
    new_version = "unknown"

    if "test" in item['tool_shed_url']:
        new_version = tts.repositories.get_ordered_installable_revisions(item['name'], item['owner'])[-1]
    else:
        new_version = ts.repositories.get_ordered_installable_revisions(item['name'], item['owner'])[-1]

    if old_version != new_version:
        print "%s\t%s\t%s\t%s" % (item['name'], item['owner'], old_version, new_version)
        item['revision'] = new_version
        if old_version != "unknown":
            sed_output.append("s/%s/%s/g" % (old_version, new_version))
    #Counter stuff here to make sure we don't poll the toolshed rest api too frequently (risk of timeouts).
    counter += 1
    if counter == 20:
        time.sleep(10)
        counter = 0

#Rewrite new tool_list with updated versions to yaml var.
whole_yaml['tools'] = tool_list

#Write out the new yaml file with updated versions.
with open(args.output, "w") as outfile:
    yaml.dump(whole_yaml, outfile, default_flow_style=False)

#Write out sed script file.
if args.sed_file:
    with open(args.sed_file, "w") as f:
        f.write("\n".join(sed_output) + "\n")
