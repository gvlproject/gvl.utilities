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
#   @Author: Simon Gladman, 2016. Modified by Madison Flannery, 2016.
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
parser.add_argument('-o','--output', help='Output file name', required=True)

args = parser.parse_args()

#Read the input yaml file
stream=open(args.input, 'r')
tools = yaml.load_all(stream)
whole_yaml=tools.next()

if args.verbose:
    print whole_yaml

tool_list=whole_yaml['tools']

# Output variables.
updated_tools = "--- UPDATED TOOLS ---\nTool\tOwner\tLatest\n"
deprecated_tools = "--- DEPRECATED TOOLS ---\nTool\tOwner\n"

#Loop through the tools and check their versions using bioblend's toolshed get_ordered_installable_revisions method
counter = 0
for item in tool_list:
    # Delete the 'revision' key if exists.
    old_version=item.pop('revision', 'unknown')

    # Create 'revisions' if need be, append old version if exists.
    if 'revisions' not in item.keys():
        item['revisions'] = []
        if old_version != 'unknown':
            item['revisions'].append(old_version)

    new_version = "unknown"

    # Get new version revision.
    if "test" in item.get('tool_shed_url', 'https://toolshed.g2.bx.psu.edu/'):
        new_version = tts.repositories.get_ordered_installable_revisions(item['name'], item['owner'])[-1]
        is_deprecated = tts.repositories.get_repository_revision_install_info(item['name'], item['owner'], new_version)[0].get('deprecated', False)
    else:
        new_version = ts.repositories.get_ordered_installable_revisions(item['name'], item['owner'])[-1]
        is_deprecated = ts.repositories.get_repository_revision_install_info(item['name'], item['owner'], new_version)[0].get('deprecated', False)

    # If tool is deprecated, add to string for stdout.
    if is_deprecated:
        deprecated_tools += "{0}\t{1}\t\n".format(item['name'], item['owner'])

    # Add and print revision if we haven't seen it before.
    if new_version not in item['revisions']:
        updated_tools += "{0}\t{1}\t{2}\n".format(item['name'], item['owner'], new_version)
        item['revisions'].append(new_version)

    # Counter stuff here to make sure we don't poll the toolshed rest api too frequently (risk of timeouts).
    counter += 1
    if counter == 20:
        time.sleep(10)
        counter = 0

# Print stdout.
print(updated_tools + "\n")
print(deprecated_tools + "\n")

#Rewrite new tool_list with updated versions to yaml var.
whole_yaml['tools'] = tool_list

#Write out the new yaml file with updated versions.
with open(args.output, "w") as outfile:
    yaml.dump(whole_yaml, outfile, default_flow_style=False)
