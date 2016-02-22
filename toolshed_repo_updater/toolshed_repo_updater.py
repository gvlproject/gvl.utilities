#!/usr/bin/env python

from bioblend import toolshed
import time
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help="Input file name", required=True)
parser.add_argument('-o','--output', help='Output file name', required=True)

args = parser.parse_args()

ts = toolshed.ToolShedInstance(url='https://toolshed.g2.bx.psu.edu')
tts = toolshed.ToolShedInstance(url='https://testtoolshed.g2.bx.psu.edu')

stream=open(args.input, 'r')
tools = yaml.load_all(stream)
tool_list=[]

for tool in tools:
    tool_list=tool['tools']

print("Tool\tOwner\tCurrent\tLatest")
counter = 0
for item in tool_list:

    tool_key = item['name']+'::'+item['owner']
    old_version=item.get('revision', 'unknown')
    new_version = "unknown"

    if "test" in item['tool_shed_url']:
        new_version = tts.repositories.get_ordered_installable_revisions(item['name'], item['owner'])[-1]
    else:
        new_version = ts.repositories.get_ordered_installable_revisions(item['name'], item['owner'])[-1]

    if old_version != new_version:
        print "%s\t%s\t%s\t%s" % (item['name'], item['owner'], old_version, new_version)
        item['revision'] = new_version

    counter += 1
    if counter == 20:
        time.sleep(5)
        counter = 0

tools['tools'] = tool_list

with open(args.output, "w") as outfile:
    yaml.dump(tools, outfile, default_flow_style=False)
