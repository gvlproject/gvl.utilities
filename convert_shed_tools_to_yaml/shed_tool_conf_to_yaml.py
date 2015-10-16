#!/usr/bin/env python

import argparse
from collections import defaultdict
import logging
from xml.etree.ElementTree import ElementTree

import yaml


log = logging.getLogger(__name__)


def write_tool_list(sections):
    target_yaml = {'api_key': '<Galaxy Admin user API key>',
                   'galaxy_instance': '<IP address for target Galaxy instance>',
                   'tools': []
                   }
    for section_id, tools in sections.iteritems():
        for tool_key, tool in tools.iteritems():
            target_yaml['tools'].append({'name': tool['name'],
                                         'owner': tool['owner'],
                                         'tool_panel_section_id': section_id,
                                         'revision': tool['revision'],
                                         'tool_shed_url': tool['tool_shed_url']})

    with open('shed_tool_list.yaml', 'w') as outfile:
        outfile.write(yaml.dump(target_yaml, default_flow_style=False))


def parse_shed_tool_conf(file):
    """
    Parses the xml in shed_tool_conf xml and returns a dictionary in the following format:
    {
        section_id: [
            name:
            owner:
            revision:
            tool_shed_url:
        ]
    }
    """
    sections = defaultdict(lambda: {})
    doc = ElementTree(file=file)
    for section in doc.findall("//section"):
        for tool in section.findall('tool'):
            sections[
                section.get('id')][
                tool.find('repository_name').text +
                '|' +
                tool.find('installed_changeset_revision').text] = {
                'name': tool.find('repository_name').text,
                'owner': tool.find('repository_owner').text,
                'revision': tool.find('installed_changeset_revision').text,
                'tool_shed_url': 'https://' +
                tool.find('tool_shed').text}
    return sections


def convert_shedtool_to_yaml(file):
    sections = parse_shed_tool_conf(file)
    write_tool_list(sections)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        required=True,
                        help="Path to <shed_tool_conf.xml> to convert")
    args = parser.parse_args()

    convert_shedtool_to_yaml(args.file)
